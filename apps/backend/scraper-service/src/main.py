from fastapi import FastAPI

from service_clients.model_client import ModelClient
from service_clients.embedding_client import EmbeddingClient
from shared_config import get_settings
from shared_logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

app = FastAPI(
    title="Vecinita Scraper Service",
    description="Data collection and orchestration service",
    version="0.1.0",
)

model_client = ModelClient(base_url=settings.model_service_url)
embedding_client = EmbeddingClient(base_url=settings.embedding_service_url)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "scraper-service"}


@app.get("/")
async def root() -> dict:
    return {"message": "Vecinita Scraper Service is running"}
