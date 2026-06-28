from src.agents.base import BaseAgent, AgentState
from src.agents.tools import query_sales, get_product_info
from src.forecasting.pipeline import ForecastPipeline


class DemandForecastAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "DemandForecastAgent"

    def run(self, state: AgentState) -> AgentState:
        forecasts = {}
        for product in state["products"]:
            pid = product["id"]
            sales_raw = query_sales.invoke({"product_id": pid, "days": 365})
            sales_df = pd.read_json(sales_raw)

            pipeline = ForecastPipeline()
            result = pipeline.run(sales_df)
            preds = pipeline.forecast(sales_df)

            forecasts[pid] = {
                "predictions": preds.tolist(),
                "model": result["model"].name,
                "metrics": result["metrics"],
            }

        state["forecasts"] = forecasts
        return state
