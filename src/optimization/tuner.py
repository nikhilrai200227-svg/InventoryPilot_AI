import numpy as np
import optuna
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit

from config.constants import OPTUNA_N_TRIALS
from src.models.base import BaseModel


def _get_param_space(trial: optuna.Trial, model_name: str) -> dict:
    if model_name == "RandomForest":
        return {
            "n_estimators": trial.suggest_int("n_estimators", 100, 500, step=50),
            "max_depth": trial.suggest_int("max_depth", 3, 20),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 2, 10),
        }
    if model_name == "XGBoost":
        return {
            "n_estimators": trial.suggest_int("n_estimators", 100, 500, step=50),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        }
    if model_name == "LightGBM":
        return {
            "n_estimators": trial.suggest_int("n_estimators", 100, 500, step=50),
            "num_leaves": trial.suggest_int("num_leaves", 15, 127),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        }
    if model_name == "CatBoost":
        return {
            "iterations": trial.suggest_int("iterations", 100, 500, step=50),
            "depth": trial.suggest_int("depth", 4, 10),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1, 10),
        }
    return {}


def optimize(
    model: BaseModel, X: np.ndarray, y: np.ndarray, n_trials: int = OPTUNA_N_TRIALS
) -> dict:
    """Run Optuna study for one model. Returns best params dict."""

    def objective(trial: optuna.Trial) -> float:
        params = _get_param_space(trial, model.name)
        # Create fresh model instance each trial to avoid CatBoost "fitted" error
        trial_model = model.__class__()
        trial_model.set_params(params)
        trial_model.train(X, y)

        tscv = TimeSeriesSplit(n_splits=3)
        maes = []
        for train_idx, val_idx in tscv.split(X):
            X_tr, X_val = X[train_idx], X[val_idx]
            y_tr, y_val = y[train_idx], y[val_idx]
            trial_model.train(X_tr, y_tr)
            preds = trial_model.predict(X_val)
            maes.append(mean_absolute_error(y_val, preds))
        return float(np.mean(maes))

    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=42))
    study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
    return study.best_params
