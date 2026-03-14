from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    """Base settings shared by all Vecinita backend services.

    List fields (e.g. cors_origins) must be provided as JSON arrays when
    set via environment variables:  CORS_ORIGINS='["http://localhost:3000"]'
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "0.0.0.0"
    port: int = 8000

    # URLs of downstream services (used by services that call others)
    scraper_service_url: str = "http://localhost:8001"
    model_service_url: str = "http://localhost:8002"
    embedding_service_url: str = "http://localhost:8003"

    # CORS — set as a JSON array string: CORS_ORIGINS='["https://example.com"]'
    cors_origins: list[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> BaseServiceSettings:
    return BaseServiceSettings()
