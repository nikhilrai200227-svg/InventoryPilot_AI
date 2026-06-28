from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database import get_db

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/levels")
def get_inventory_levels(db: Session = Depends(get_db)):
    """Current stock levels for all products."""
    rows = db.execute(
        text("""
            SELECT p.id, p.sku, p.name, p.category,
                   ir.quantity_on_hand, ir.record_date
            FROM products p
            LEFT JOIN (
                SELECT product_id, quantity_on_hand, record_date,
                       ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY record_date DESC) AS rn
                FROM inventory_records
            ) ir ON p.id = ir.product_id AND ir.rn = 1
            ORDER BY p.sku
        """)
    ).fetchall()
    return [dict(r._mapping) for r in rows]


@router.get("/stockout-risk")
def get_stockout_risks(db: Session = Depends(get_db)):
    """Stockout risk for all products."""
    rows = db.execute(
        text("""
            WITH current_stock AS (
                SELECT product_id, quantity_on_hand,
                       ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY record_date DESC) AS rn
                FROM inventory_records
            ),
            avg_sales AS (
                SELECT product_id, AVG(quantity_sold) AS daily_avg
                FROM sales_transactions
                WHERE transaction_date >= DATE('now', '-30 days')
                GROUP BY product_id
            )
            SELECT cs.product_id, p.sku, p.name,
                   cs.quantity_on_hand,
                   COALESCE(asl.daily_avg, 0) AS daily_avg_sales,
                   CASE
                       WHEN COALESCE(asl.daily_avg, 0) = 0 THEN 'unknown'
                       WHEN cs.quantity_on_hand / asl.daily_avg < 7 THEN 'high'
                       WHEN cs.quantity_on_hand / asl.daily_avg < 14 THEN 'medium'
                       ELSE 'low'
                   END AS risk_level
            FROM current_stock cs
            JOIN products p ON cs.product_id = p.id
            LEFT JOIN avg_sales asl ON cs.product_id = asl.product_id
            WHERE cs.rn = 1
            ORDER BY risk_level DESC, cs.quantity_on_hand ASC
        """)
    ).fetchall()
    return [dict(r._mapping) for r in rows]
