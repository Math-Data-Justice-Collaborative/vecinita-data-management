from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared_config import get_settings
from shared_logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

app = FastAPI(
    title="Vecinita Proxy",
    description="API gateway and BFF for the Vecinita platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "proxy"}


@app.get("/")
async def root() -> dict:
    return {"message": "Vecinita Proxy is running"}
