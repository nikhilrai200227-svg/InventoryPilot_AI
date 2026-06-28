from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Base, engine
from config.settings import settings

from app.api.v1 import forecast, inventory, explain, reports, assistant


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    from src.database import SessionLocal
    from src.models.product import Product
    db = SessionLocal()
    if db.query(Product).count() == 0:
        from scripts.seed_data import seed
        seed()
    db.close()
    yield


app = FastAPI(
    title="InventoryPilot AI",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forecast.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
app.include_router(explain.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(assistant.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "model": settings.gemini_model}
