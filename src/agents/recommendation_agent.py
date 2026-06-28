import json

from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.base import BaseAgent, AgentState


RECOMMENDATION_PROMPT = """You are an inventory optimization expert. Based on the forecasts, 
inventory analysis, and SHAP explanations provided, generate 3-5 actionable business recommendations.

For each recommendation include:
1. **Action** — what to do (e.g., "Increase safety stock for SKU-123")
2. **Rationale** — why (data-driven justification)
3. **Impact** — expected outcome (reduce stockouts by X%, save $Y)

Be specific, use numbers, and prioritize by urgency."""


class BusinessRecommendationAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "BusinessRecommendationAgent"

    def run(self, state: AgentState) -> AgentState:
        context = {
            "forecasts": state.get("forecasts", {}),
            "analysis": state.get("analysis", {}),
            "explanations": state.get("explanations", {}),
        }

        prompt = self.build_prompt(RECOMMENDATION_PROMPT, state)
        prompt += f"\n\nData:\n{json.dumps(context, default=str, indent=2)}"

        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content="Generate inventory recommendations based on the latest data."),
        ]
        response = self.llm.invoke(messages)

        state["recommendations"] = [response.content]
        return state
