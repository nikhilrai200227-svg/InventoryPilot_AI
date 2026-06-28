import numpy as np
import xgboost as xgb

from src.models.base import BaseModel


class XGBoostModel(BaseModel):
    def __init__(self, **kwargs):
        self.model = xgb.XGBRegressor(
            n_estimators=kwargs.get("n_estimators", 300),
            max_depth=kwargs.get("max_depth", 6),
            learning_rate=kwargs.get("learning_rate", 0.05),
            subsample=kwargs.get("subsample", 0.8),
            colsample_bytree=kwargs.get("colsample_bytree", 0.8),
            random_state=42,
            n_jobs=-1,
        )

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        self.model.fit(X_train, y_train)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def get_params(self) -> dict:
        return self.model.get_params()

    def set_params(self, params: dict) -> None:
        valid = {k: v for k, v in params.items() if k in self.model.get_params()}
        self.model.set_params(**valid)

    @property
    def name(self) -> str:
        return "XGBoost"
