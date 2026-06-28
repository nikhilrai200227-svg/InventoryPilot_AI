from datetime import date
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    sku: str
    name: str
    category: str
    unit_price: float = Field(gt=0)
    lead_time_days: int = Field(default=7, ge=1)
    safety_stock: int = Field(default=0, ge=0)


class ProductResponse(ProductCreate):
    id: int

    model_config = {"from_attributes": True}


class ForecastRequest(BaseModel):
    product_id: int
    days_ahead: int = Field(default=30, ge=1, le=365)
    model_type: str | None = None  # auto-select if None


class ForecastResponse(BaseModel):
    product_id: int
    forecast_dates: list[str]
    forecast_values: list[float]
    confidence_lower: list[float] | None = None
    confidence_upper: list[float] | None = None
    model_used: str
    metrics: dict | None = None


class ExplainRequest(BaseModel):
    product_id: int
    forecast_date: str


class ShapResponse(BaseModel):
    product_id: int
    expected_value: float
    feature_names: list[str]
    shap_values: list[float]
    waterfall_plot: str | None = None  # base64 encoded
