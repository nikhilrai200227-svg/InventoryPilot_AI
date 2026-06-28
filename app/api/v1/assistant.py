from fastapi import APIRouter
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from config.settings import settings

router = APIRouter(prefix="/assistant", tags=["assistant"])


class ChatRequest(BaseModel):
    message: str
    context: str | None = None


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(req: ChatRequest):
    """Ask inventory-related questions to the Gemini-powered assistant."""
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.gemini_api_key,
        temperature=0.3,
    )

    system = "You are an inventory intelligence assistant. Answer questions about inventory, demand forecasting, and supply chain using data-driven insights."
    if req.context:
        system += f"\n\nCurrent context:\n{req.context}"

    response = llm.invoke(system + "\n\nUser: " + req.message)
    return ChatResponse(reply=response.content)
