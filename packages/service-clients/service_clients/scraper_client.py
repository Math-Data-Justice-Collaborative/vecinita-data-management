import httpx
from pydantic import HttpUrl

from shared_schemas.scraper import ScrapeRequest, ScrapeResult


class ScraperClient:
    """Async HTTP client for the Vecinita scraper-service."""

    def __init__(self, base_url: str, timeout: float = 60.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def scrape(self, url: str, depth: int = 1) -> ScrapeResult:
        """Send a scrape request to scraper-service."""
        payload = ScrapeRequest(url=HttpUrl(url), depth=depth)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/scrape",
                content=payload.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return ScrapeResult.model_validate(response.json())

    async def health(self) -> dict:
        """Check scraper-service health."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
