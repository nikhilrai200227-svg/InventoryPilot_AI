from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from config.constants import DATA_RAW
from src.database import SessionLocal
from src.models.product import Product
from src.models.inventory import InventoryRecord, SalesTransaction


def load_products_csv(filepath: str | Path) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    required = {"sku", "name", "category", "unit_price"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df


def load_sales_csv(filepath: str | Path) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=["transaction_date"])
    required = {"product_id", "transaction_date", "quantity_sold", "unit_price"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df


def seed_products_from_csv(filepath: str | Path, db: Session) -> int:
    df = load_products_csv(filepath)
    count = 0
    for _, row in df.iterrows():
        exists = db.query(Product).filter(Product.sku == row["sku"]).first()
        if not exists:
            db.add(
                Product(
                    sku=row["sku"],
                    name=row["name"],
                    category=row["category"],
                    unit_price=row["unit_price"],
                    lead_time_days=int(row.get("lead_time_days", 7)),
                    safety_stock=int(row.get("safety_stock", 0)),
                )
            )
            count += 1
    db.commit()
    return count


def seed_sales_from_csv(filepath: str | Path, db: Session) -> int:
    df = load_sales_csv(filepath)
    df.to_sql("sales_transactions", db.bind, if_exists="append", index=False)
    return len(df)
