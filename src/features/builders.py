import numpy as np
import pandas as pd


def add_lag_features(df: pd.DataFrame, cols: list[str], lags: list[int]) -> pd.DataFrame:
    """Shift target values backward in time so the model sees past sales."""
    df = df.copy()
    for col in cols:
        for lag in lags:
            df[f"{col}_lag_{lag}"] = df[col].shift(lag)
    return df


def add_rolling_features(
    df: pd.DataFrame, cols: list[str], windows: list[int]
) -> pd.DataFrame:
    """Rolling mean / std smooth out noise and capture recent trends."""
    df = df.copy()
    for col in cols:
        for w in windows:
            df[f"{col}_roll_mean_{w}"] = df[col].shift(1).rolling(w).mean()
            df[f"{col}_roll_std_{w}"] = df[col].shift(1).rolling(w).std()
    return df


def add_date_features(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """Calendar signals — day-of-week, month, quarter, weekend flag."""
    dt = pd.to_datetime(df[date_col])
    df["day_of_week"] = dt.dt.dayofweek
    df["month"] = dt.dt.month
    df["quarter"] = dt.dt.quarter
    df["is_weekend"] = dt.dt.dayofweek.isin([5, 6]).astype(int)
    df["day_of_year"] = dt.dt.dayofyear
    return df


def build_features(
    sales: pd.DataFrame, date_col: str = "transaction_date", target: str = "quantity_sold"
) -> pd.DataFrame:
    """End-to-end feature pipeline for a single product's sales series."""
    df = sales.sort_values(date_col).reset_index(drop=True)

    df = add_date_features(df, date_col)
    df = add_lag_features(df, [target], lags=[1, 2, 3, 7, 14, 28])
    df = add_rolling_features(df, [target], windows=[7, 14, 28])

    df.dropna(inplace=True)
    return df
