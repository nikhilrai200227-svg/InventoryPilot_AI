from src.agents.base import BaseAgent, AgentState
from src.agents.tools import query_sales, get_product_info
from src.explainability.shap_explainer import ShapExplainer
from src.features.builders import build_features
from src.models.random_forest import RandomForestModel


class ExplainabilityAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "ExplainabilityAgent"

    def run(self, state: AgentState) -> AgentState:
        if not state.get("forecasts"):
            return state

        explainer = ShapExplainer()
        explanations = {}

        sample_product_id = list(state["forecasts"].keys())[0]
        sales_raw = query_sales.invoke({"product_id": sample_product_id, "days": 365})
        sales_df = pd.read_json(sales_raw)
        df = build_features(sales_df)

        feature_cols = [c for c in df.columns if c not in ("transaction_date", "quantity_sold")]
        X = df[feature_cols].values
        y = df["quantity_sold"].values

        model = RandomForestModel()
        model.train(X, y)

        explanation = explainer.explain(model, X, feature_cols)
        explanations[sample_product_id] = explanation

        state["explanations"] = explanations
        return state
