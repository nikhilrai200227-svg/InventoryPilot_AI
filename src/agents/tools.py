import json

import pandas as pd
from langchain_core.tools import tool
from sqlalchemy import text

from src.database import SessionLocal


@tool
def query_inventory(product_id: int | None = None) -> str:
    """Fetch current inventory levels. Optionally filter by product_id."""
    with SessionLocal() as db:
        if product_id:
            result = db.execute(
                text("SELECT * FROM inventory_records WHERE product_id = :pid ORDER BY record_date DESC LIMIT 30"),
                {"pid": product_id},
            )
        else:
            result = db.execute(
                text("SELECT * FROM inventory_records ORDER BY record_date DESC LIMIT 100")
            )
        rows = [dict(row._mapping) for row in result]
    return json.dumps(rows, default=str)


@tool
def query_sales(product_id: int, days: int = 90) -> str:
    """Fetch recent sales history for a product."""
    with SessionLocal() as db:
        result = db.execute(
            text("""
                SELECT * FROM sales_transactions
                WHERE product_id = :pid
                AND transaction_date >= DATE('now', :days_ago)
                ORDER BY transaction_date
            """),
            {"pid": product_id, "days_ago": f"-{days} days"},
        )
        rows = [dict(row._mapping) for row in result]
    return json.dumps(rows, default=str)


@tool
def get_product_info(sku: str | None = None) -> str:
    """Look up product metadata by SKU or list all products."""
    with SessionLocal() as db:
        if sku:
            result = db.execute(
                text("SELECT * FROM products WHERE sku = :sku"), {"sku": sku}
            )
        else:
            result = db.execute(text("SELECT * FROM products LIMIT 50"))
        rows = [dict(row._mapping) for row in result]
    return json.dumps(rows, default=str)


@tool
def get_stockout_risk(product_id: int) -> str:
    """Calculate stockout risk based on current stock vs average daily sales."""
    with SessionLocal() as db:
        inv = db.execute(
            text("SELECT quantity_on_hand FROM inventory_records WHERE product_id = :pid ORDER BY record_date DESC LIMIT 1"),
            {"pid": product_id},
        ).scalar()

        avg_daily = db.execute(
            text("""
                SELECT AVG(quantity_sold) FROM sales_transactions
                WHERE product_id = :pid
                AND transaction_date >= DATE('now', '-30 days')
            """),
            {"pid": product_id},
        ).scalar()

    if inv is None or avg_daily is None or avg_daily == 0:
        return json.dumps({"risk": "unknown", "days_remaining": None})

    days_remaining = inv / avg_daily
    risk = "high" if days_remaining < 7 else "medium" if days_remaining < 14 else "low"
    return json.dumps({"risk": risk, "days_remaining": round(days_remaining, 1)})
