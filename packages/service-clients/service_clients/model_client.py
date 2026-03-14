import httpx

from shared_schemas.model import PredictRequest, PredictResponse


class ModelClient:
    """Async HTTP client for the Vecinita model-service."""

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def predict(self, text: str, model_version: str | None = None) -> PredictResponse:
        """Send a prediction request to model-service."""
        payload = PredictRequest(text=text, model_version=model_version)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/predict",
                content=payload.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return PredictResponse.model_validate(response.json())

    async def health(self) -> dict:
        """Check model-service health."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
