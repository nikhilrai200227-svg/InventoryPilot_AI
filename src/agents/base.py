from abc import ABC, abstractmethod
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool


class AgentState(dict):
    """Shared state passed between agents in the LangGraph workflow."""
    messages: list = []
    products: list = []
    forecasts: dict = {}
    explanations: dict = {}
    recommendations: list = []
    report: str = ""
    error: str | None = None


class BaseAgent(ABC):
    """Every agent shares a name, an LLM, a list of tools, and a run method."""

    def __init__(self, llm: BaseChatModel, tools: list[BaseTool] | None = None):
        self.llm = llm
        self.tools = tools or []

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def run(self, state: AgentState) -> AgentState: ...

    def build_prompt(self, system_prompt: str, state: AgentState) -> str:
        context = f"""
Products: {len(state['products'])} loaded
Forecasts available: {list(state['forecasts'].keys())}
Existing recommendations: {len(state['recommendations'])}
"""
        return system_prompt + "\n\nContext:\n" + context
