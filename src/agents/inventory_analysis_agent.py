from src.agents.base import BaseAgent, AgentState
from src.agents.tools import query_inventory, get_stockout_risk


class InventoryAnalysisAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "InventoryAnalysisAgent"

    def run(self, state: AgentState) -> AgentState:
        analysis = {}
        for product in state["products"]:
            pid = product["id"]
            inv_data = query_inventory.invoke({"product_id": pid})
            risk = get_stockout_risk.invoke({"product_id": pid})

            analysis[pid] = {
                "inventory": inv_data,
                "stockout_risk": risk,
            }

        state["analysis"] = analysis
        return state
