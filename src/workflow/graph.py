from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from config.settings import settings
from src.agents.base import AgentState
from src.agents.demand_forecast_agent import DemandForecastAgent
from src.agents.inventory_analysis_agent import InventoryAnalysisAgent
from src.agents.explainability_agent import ExplainabilityAgent
from src.agents.recommendation_agent import BusinessRecommendationAgent
from src.agents.report_agent import ExecutiveReportAgent
from src.agents.tools import (
    query_inventory,
    query_sales,
    get_product_info,
    get_stockout_risk,
)


def _build_llm():
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.gemini_api_key,
        temperature=0.2,
    )


_shared_tools = [query_inventory, query_sales, get_product_info, get_stockout_risk]


def _node_fn(agent_cls):
    """Factory: creates a graph node from an agent class."""
    def node(state: AgentState) -> AgentState:
        llm = _build_llm()
        agent = agent_cls(llm=llm, tools=_shared_tools)
        return agent.run(state)
    node.__name__ = agent_cls.__name__
    return node


def build_graph() -> StateGraph:
    """Build the agentic workflow graph.

    Flow: forecast → analyze → explain → recommend → report → END
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("forecast", _node_fn(DemandForecastAgent))
    workflow.add_node("analyze", _node_fn(InventoryAnalysisAgent))
    workflow.add_node("explain", _node_fn(ExplainabilityAgent))
    workflow.add_node("recommend", _node_fn(BusinessRecommendationAgent))
    workflow.add_node("report", _node_fn(ExecutiveReportAgent))

    workflow.set_entry_point("forecast")

    workflow.add_edge("forecast", "analyze")
    workflow.add_edge("analyze", "explain")
    workflow.add_edge("explain", "recommend")
    workflow.add_edge("recommend", "report")
    workflow.add_edge("report", END)

    return workflow.compile(checkpointer=MemorySaver())
