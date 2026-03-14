from fastapi import FastAPI

from shared_schemas.model import PredictRequest, PredictResponse
from shared_config import get_settings
from shared_logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

app = FastAPI(
    title="Vecinita Model Service",
    description="ML model inference service",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "model-service"}


@app.get("/")
async def root() -> dict:
    return {"message": "Vecinita Model Service is running"}


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest) -> PredictResponse:
    logger.info("Running inference", extra={"input_length": len(request.text)})
    # TODO: load model and run inference
    return PredictResponse(label="unknown", score=0.0)
