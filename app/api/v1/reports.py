import json

from fastapi import APIRouter, Depends
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy import text
from sqlalchemy.orm import Session

from config.settings import settings
from src.database import get_db

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate")
def generate_report(db: Session = Depends(get_db)):
    """Generate executive report using Gemini."""
    products = db.execute(text("SELECT * FROM products LIMIT 10")).fetchall()
    products_data = [dict(p._mapping) for p in products]

    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.gemini_api_key,
        temperature=0.2,
    )

    prompt = f"""You are an executive report writer.
Generate a professional supply chain report based on {len(products_data)} products.

Products: {json.dumps(products_data, default=str)}

Structure: Executive Summary → Inventory Health → Recommendations → Methodology"""

    response = llm.invoke(prompt)
    return {"report": response.content}
