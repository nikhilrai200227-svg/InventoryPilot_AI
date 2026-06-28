"""Seed the database with sample products and sales data for demo purposes."""

import random
from datetime import date, timedelta

import numpy as np

from src.database import SessionLocal, Base, engine
from src.models.product import Product
from src.models.inventory import InventoryRecord, SalesTransaction


PRODUCTS = [
    {"sku": "WHL-001", "name": "Organic Wheat Flour", "category": "Grains", "unit_price": 12.99, "lead_time_days": 5, "safety_stock": 50},
    {"sku": "RCE-002", "name": "Basmati Rice 5kg", "category": "Grains", "unit_price": 18.50, "lead_time_days": 7, "safety_stock": 30},
    {"sku": "OIL-003", "name": "Olive Oil 1L", "category": "Oils", "unit_price": 24.99, "lead_time_days": 10, "safety_stock": 20},
    {"sku": "SPC-004", "name": "Cinnamon Powder", "category": "Spices", "unit_price": 8.99, "lead_time_days": 14, "safety_stock": 40},
    {"sku": "DAL-005", "name": "Red Lentils 2kg", "category": "Legumes", "unit_price": 6.99, "lead_time_days": 6, "safety_stock": 60},
    {"sku": "TEA-006", "name": "Assam Black Tea", "category": "Beverages", "unit_price": 14.99, "lead_time_days": 8, "safety_stock": 25},
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    existing = db.query(Product).count()
    if existing > 0:
        print(f"Database already has {existing} products. Skipping seed.")
        db.close()
        return

    products = []
    for p in PRODUCTS:
        product = Product(**p)
        db.add(product)
        db.flush()
        products.append(product)

    today = date.today()
    for product in products:
        base_demand = random.randint(20, 80)
        # 365 days of sales with weekly seasonality and random noise
        for i in range(365):
            day = today - timedelta(days=365 - i)
            day_of_week = day.weekday()
            multiplier = 0.7 if day_of_week in (5, 6) else 1.0  # lower on weekends
            noise = np.random.normal(0, 0.15)
            qty = max(0, int(base_demand * multiplier * (1 + noise)))
            db.add(SalesTransaction(
                product_id=product.id,
                transaction_date=day,
                quantity_sold=qty,
                unit_price=product.unit_price,
                total_amount=round(qty * product.unit_price, 2),
            ))

        # Weekly inventory snapshots
        for i in range(52):
            day = today - timedelta(weeks=52 - i)
            stock = random.randint(
                max(10, product.safety_stock - 10),
                product.safety_stock + random.randint(20, 100),
            )
            db.add(InventoryRecord(
                product_id=product.id,
                record_date=day,
                quantity_on_hand=stock,
                quantity_reserved=random.randint(0, 10),
            ))

    db.commit()
    db.close()
    print(f"Seeded {len(products)} products with 365 days of sales and 52 weeks of inventory.")


if __name__ == "__main__":
    seed()
