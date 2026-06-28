import numpy as np
from catboost import CatBoostRegressor

from src.models.base import BaseModel


class CatBoostModel(BaseModel):
    def __init__(self, **kwargs):
        self.model = CatBoostRegressor(
            iterations=kwargs.get("iterations", 300),
            depth=kwargs.get("depth", 6),
            learning_rate=kwargs.get("learning_rate", 0.05),
            l2_leaf_reg=kwargs.get("l2_leaf_reg", 3),
            random_seed=42,
            verbose=False,
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
        return "CatBoost"
