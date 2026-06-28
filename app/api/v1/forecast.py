import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database import get_db
from src.forecasting.pipeline import ForecastPipeline
from src.schemas import ForecastRequest, ForecastResponse

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.post("/run")
def run_forecast(req: ForecastRequest, db: Session = Depends(get_db)):
    """Train models and generate forecast for a product."""
    rows = db.execute(
        text("""
            SELECT transaction_date, quantity_sold
            FROM sales_transactions
            WHERE product_id = :pid
            ORDER BY transaction_date
        """),
        {"pid": req.product_id},
    ).fetchall()

    if not rows:
        return {"error": "No sales data found for this product"}

    sales_df = pd.DataFrame(
        [{"transaction_date": r[0], "quantity_sold": r[1]} for r in rows]
    )

    pipeline = ForecastPipeline(model_type=req.model_type)
    result = pipeline.run(sales_df)
    preds = pipeline.forecast(sales_df, steps=req.days_ahead)

    return ForecastResponse(
        product_id=req.product_id,
        forecast_dates=[str(d) for d in pd.date_range(start=sales_df["transaction_date"].iloc[-1], periods=req.days_ahead + 1)[1:]],
        forecast_values=preds.tolist(),
        model_used=result["model"].name,
        metrics=result["metrics"],
    )
