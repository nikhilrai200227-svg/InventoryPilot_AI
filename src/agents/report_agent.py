import json

from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.base import BaseAgent, AgentState


REPORT_PROMPT = """You are an executive report writer for a supply chain intelligence platform.
Synthesize the following data into a professional executive report.

Structure:
1. **Executive Summary** — top-level overview
2. **Demand Forecast Highlights** — key trends and anomalies
3. **Inventory Health** — stockout risks, overstock positions
4. **Key Recommendations** — top 3 actions leadership should take
5. **Methodology** — models used, data timeframe

Write in a clear, professional tone suitable for a VP of Supply Chain."""


class ExecutiveReportAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "ExecutiveReportAgent"

    def run(self, state: AgentState) -> AgentState:
        context = {
            "forecasts": state.get("forecasts", {}),
            "analysis": state.get("analysis", {}),
            "explanations": state.get("explanations", {}),
            "recommendations": state.get("recommendations", []),
        }

        prompt = self.build_prompt(REPORT_PROMPT, state)
        prompt += f"\n\nData:\n{json.dumps(context, default=str, indent=2)}"

        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content="Generate the executive report."),
        ]
        response = self.llm.invoke(messages)

        state["report"] = response.content
        return state
