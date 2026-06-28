from abc import ABC, abstractmethod

import numpy as np


class BaseModel(ABC):
    """Every model must implement train + predict + get_params."""

    @abstractmethod
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None: ...

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray: ...

    @abstractmethod
    def get_params(self) -> dict: ...

    @abstractmethod
    def set_params(self, params: dict) -> None: ...

    @property
    @abstractmethod
    def name(self) -> str: ...
