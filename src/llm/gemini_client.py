from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from config.settings import settings


class GeminiClient:
    """Wrapper around Gemini for inventory-specific interactions."""

    def __init__(self, temperature: float = 0.2):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.gemini_api_key,
            temperature=temperature,
        )

    def chat(self, message: str, context: str | None = None) -> str:
        system = (
            "You are an inventory intelligence assistant. "
            "Answer questions about demand forecasting, stock levels, "
            "reorder points, and supply chain optimization using data."
        )
        if context:
            system += f"\n\nRelevant data:\n{context}"

        messages = [
            SystemMessage(content=system),
            HumanMessage(content=message),
        ]
        response = self.llm.invoke(messages)
        return response.content

    def generate_recommendations(self, data_summary: str) -> str:
        prompt = (
            "Based on the following inventory data, provide 3-5 actionable "
            "business recommendations. Be specific and include expected impact.\n\n"
            f"Data:\n{data_summary}"
        )
        return self.chat(prompt)

    def generate_executive_report(self, data_summary: str) -> str:
        prompt = (
            "Generate a professional executive report for VP of Supply Chain. "
            "Include: Executive Summary, Forecast Highlights, Inventory Health, "
            "Key Recommendations, Methodology.\n\n"
            f"Data:\n{data_summary}"
        )
        return self.chat(prompt)
