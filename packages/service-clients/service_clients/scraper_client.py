from httpx import AsyncClient, HTTPStatusError, RequestError
from pydantic import HttpUrl

from shared_schemas.scraper import ScrapeRequest, ScrapeResult

_UPSTREAM_5XX_MESSAGE = "Upstream scraper service returned an error; verify scraper health and SCRAPER_SERVICE_BASE_URL."
_CLIENT_REJECTION_MESSAGE = "Scraper rejected the request."
_UNREACHABLE_MESSAGE = "Scraper service unreachable; verify SCRAPER_SERVICE_BASE_URL and network connectivity."


class ScraperUpstreamError(Exception):
    """Stable, client-safe failure from scraper HTTP calls (see FR-002 in platform spec)."""

    def __init__(self, message: str, *, mapped_http_status: int | None = None) -> None:
        self.mapped_http_status = mapped_http_status
        super().__init__(message)


def _map_http_status_error(exc: HTTPStatusError) -> ScraperUpstreamError:
    resp = exc.response
    code = resp.status_code if resp is not None else None
    if code is not None and code >= 500:
        return ScraperUpstreamError(_UPSTREAM_5XX_MESSAGE, mapped_http_status=502)
    return ScraperUpstreamError(_CLIENT_REJECTION_MESSAGE, mapped_http_status=code)


class ScraperClient:
    """Async HTTP client for the Vecinita scraper-service."""

    def __init__(self, base_url: str, timeout: float = 60.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def scrape(self, url: str, depth: int = 1) -> ScrapeResult:
        """Send a scrape request to scraper-service."""
        payload = ScrapeRequest(url=HttpUrl(url), depth=depth)
        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/scrape",
                    content=payload.model_dump_json(),
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                return ScrapeResult.model_validate(response.json())
        except HTTPStatusError as exc:
            raise _map_http_status_error(exc) from exc
        except RequestError as exc:
            raise ScraperUpstreamError(
                _UNREACHABLE_MESSAGE, mapped_http_status=503
            ) from exc

    async def health(self) -> dict:
        """Check scraper-service health."""
        try:
            async with AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/health")
                response.raise_for_status()
                return response.json()
        except HTTPStatusError as exc:
            raise _map_http_status_error(exc) from exc
        except RequestError as exc:
            raise ScraperUpstreamError(
                _UNREACHABLE_MESSAGE, mapped_http_status=503
            ) from exc
