import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, root_mean_squared_error
from sklearn.model_selection import train_test_split

from config.constants import FORECAST_HORIZON, TRAIN_TEST_SPLIT_RATIO
from src.features.builders import build_features
from src.models.base import BaseModel
from src.models.random_forest import RandomForestModel
from src.models.xgboost_model import XGBoostModel
from src.models.lightgbm_model import LightGBMModel
from src.models.catboost_model import CatBoostModel
from src.optimization.tuner import optimize


def _get_all_models() -> list[BaseModel]:
    return [
        RandomForestModel(),
        XGBoostModel(),
        LightGBMModel(),
        CatBoostModel(),
    ]


def evaluate_model(model: BaseModel, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    preds = model.predict(X_test)
    return {
        "mae": mean_absolute_error(y_test, preds),
        "rmse": root_mean_squared_error(y_test, preds),
        "mape": mean_absolute_percentage_error(y_test, preds),
    }


class ForecastPipeline:
    """End-to-end pipeline: prepare → tune → train → select → predict."""

    def __init__(self, model_type: str | None = None):
        self.model_type = model_type
        self.best_model: BaseModel | None = None
        self.metrics: dict = {}
        self.feature_cols: list[str] = []

    def run(self, sales: pd.DataFrame) -> dict:
        df = build_features(sales)

        feature_cols = [c for c in df.columns if c not in ("transaction_date", "quantity_sold")]
        self.feature_cols = feature_cols

        X = df[feature_cols].values
        y = df["quantity_sold"].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=1 - TRAIN_TEST_SPLIT_RATIO, shuffle=False
        )

        models = _get_all_models()
        if self.model_type:
            models = [m for m in models if m.name.lower() == self.model_type.lower()]

        results = []
        tuned_params = None

        for model in models:
            try:
                best_params = optimize(model, X_train, y_train)
            except Exception as e:
                continue

            model.set_params(best_params)
            model.train(X_train, y_train)
            metrics = evaluate_model(model, X_test, y_test)
            results.append((model, metrics, best_params))

        if not results:
            raise RuntimeError("No model trained successfully.")

        results.sort(key=lambda x: x[1]["mae"])
        self.best_model, self.metrics, tuned_params = results[0]
        self.best_model.train(X_train, y_train)  # retrain on full train set

        return {
            "model": self.best_model,
            "metrics": self.metrics,
            "best_params": tuned_params,
        }

    def forecast(self, sales: pd.DataFrame, steps: int = FORECAST_HORIZON) -> np.ndarray:
        """Multi-step recursive forecast by rebuilding features each step."""
        if self.best_model is None:
            raise RuntimeError("Run pipeline first.")

        history = sales.copy()
        history["transaction_date"] = pd.to_datetime(history["transaction_date"])
        predictions = []

        for _ in range(steps):
            df = build_features(history)
            last_row = df[self.feature_cols].iloc[-1:].values
            pred = float(self.best_model.predict(last_row)[0])
            predictions.append(pred)

            new_row = pd.DataFrame([{
                "transaction_date": history["transaction_date"].iloc[-1] + pd.Timedelta(days=1),
                "quantity_sold": pred,
            }])
            history = pd.concat([history, new_row], ignore_index=True)

        return np.array(predictions)
