from datetime import date, datetime

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class InventoryRecord(Base):
    __tablename__ = "inventory_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    record_date: Mapped[date] = mapped_column(Date)
    quantity_on_hand: Mapped[int] = mapped_column(Integer)
    quantity_reserved: Mapped[int] = mapped_column(Integer, default=0)
    warehouse: Mapped[str] = mapped_column(String(50), default="main")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class SalesTransaction(Base):
    __tablename__ = "sales_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    transaction_date: Mapped[date] = mapped_column(Date)
    quantity_sold: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)
    total_amount: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
