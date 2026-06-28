import numpy as np
import shap

from src.models.base import BaseModel


class ShapExplainer:
    """Wrap SHAP for model-agnostic global + local explanations."""

    def __init__(self):
        self.explainer = None
        self.shap_values = None
        self.feature_names: list[str] = []
        self.expected_value: float = 0.0

    def explain(
        self,
        model: BaseModel,
        X: np.ndarray,
        feature_names: list[str],
        background_size: int = 100,
    ) -> dict:
        """Compute SHAP values for the given model and data."""
        self.feature_names = feature_names

        # Use a subset of background data for KernelExplainer speed
        if X.shape[0] > background_size:
            background = X[np.random.choice(X.shape[0], background_size, replace=False)]
        else:
            background = X

        self.explainer = shap.KernelExplainer(model.predict, background)
        self.shap_values = self.explainer.shap_values(X[:50])  # explain first 50
        self.expected_value = float(self.explainer.expected_value)

        # Global feature importance (mean |SHAP| per feature)
        mean_shap = np.abs(self.shap_values).mean(axis=0)
        importance = {
            feature_names[i]: float(mean_shap[i])
            for i in range(len(feature_names))
        }

        # Local explanation for the first prediction
        local = {
            "expected_value": self.expected_value,
            "features": {
                feature_names[i]: float(self.shap_values[0][i])
                for i in range(len(feature_names))
            },
        }

        return {
            "global_importance": importance,
            "local_explanation": local,
            "feature_names": feature_names,
        }
