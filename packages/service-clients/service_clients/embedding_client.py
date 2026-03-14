import httpx

from shared_schemas.embedding import EmbedRequest, EmbedResponse


class EmbeddingClient:
    """Async HTTP client for the Vecinita embedding-service."""

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def embed(self, text: str, model_version: str | None = None) -> EmbedResponse:
        """Send an embedding request to embedding-service."""
        payload = EmbedRequest(text=text, model_version=model_version)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/embed",
                content=payload.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return EmbedResponse.model_validate(response.json())

    async def health(self) -> dict:
        """Check embedding-service health."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
