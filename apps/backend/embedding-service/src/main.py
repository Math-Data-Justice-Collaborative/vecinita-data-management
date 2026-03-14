from fastapi import FastAPI

from shared_schemas.embedding import EmbedRequest, EmbedResponse
from shared_config import get_settings
from shared_logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

app = FastAPI(
    title="Vecinita Embedding Service",
    description="Text embedding and vectorization service",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "embedding-service"}


@app.get("/")
async def root() -> dict:
    return {"message": "Vecinita Embedding Service is running"}


@app.post("/embed", response_model=EmbedResponse)
async def embed(request: EmbedRequest) -> EmbedResponse:
    logger.info("Generating embedding", extra={"input_length": len(request.text)})
    # TODO: load embedding model and generate vector
    return EmbedResponse(embedding=[])
