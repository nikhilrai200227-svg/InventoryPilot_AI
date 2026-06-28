import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database import get_db
from src.explainability.shap_explainer import ShapExplainer
from src.features.builders import build_features
from src.models.random_forest import RandomForestModel
from src.schemas import ExplainRequest, ShapResponse

router = APIRouter(prefix="/explain", tags=["explain"])


@router.post("/prediction")
def explain_prediction(req: ExplainRequest, db: Session = Depends(get_db)):
    """Generate SHAP explanation for a product's forecast."""
    rows = db.execute(
        text("""
            SELECT transaction_date, quantity_sold
            FROM sales_transactions
            WHERE product_id = :pid
            ORDER BY transaction_date
        """),
        {"pid": req.product_id},
    ).fetchall()

    sales_df = pd.DataFrame(
        [{"transaction_date": r[0], "quantity_sold": r[1]} for r in rows]
    )
    df = build_features(sales_df)

    feature_cols = [c for c in df.columns if c not in ("transaction_date", "quantity_sold")]
    X = df[feature_cols].values
    y = df["quantity_sold"].values

    model = RandomForestModel()
    model.train(X, y)

    explainer = ShapExplainer()
    explanation = explainer.explain(model, X, feature_cols)

    return {
        "product_id": req.product_id,
        "expected_value": explanation["local_explanation"]["expected_value"],
        "feature_names": explanation["feature_names"],
        "global_importance": explanation["global_importance"],
        "local_shap_values": explanation["local_explanation"]["features"],
    }
