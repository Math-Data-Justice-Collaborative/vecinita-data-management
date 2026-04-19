from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    """Base settings shared by all Vecinita backend services.

    List fields (e.g. cors_origins) must be provided as JSON arrays when
    set via environment variables:  ALLOWED_ORIGINS='["http://localhost:3000"]'
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    host: str = "0.0.0.0"
    port: int = 8000

    # URLs of downstream services (used by services that call others).
    # Contract names (003-consolidate-scraper-dm) are accepted alongside legacy VECINITA_* env vars.
    scraper_service_url: str = Field(
        "http://localhost:8001",
        validation_alias=AliasChoices(
            "SCRAPER_SERVICE_BASE_URL",
            "VECINITA_SCRAPER_API_URL",
        ),
    )
    model_service_url: str = Field(
        "http://localhost:8002",
        validation_alias=AliasChoices(
            "MODEL_SERVICE_BASE_URL",
            "VECINITA_MODEL_API_URL",
        ),
    )
    embedding_service_url: str = Field(
        "http://localhost:8003",
        validation_alias=AliasChoices(
            "EMBEDDING_SERVICE_BASE_URL",
            "VECINITA_EMBEDDING_API_URL",
        ),
    )

    # CORS — set as a JSON array string: ALLOWED_ORIGINS='["https://example.com"]'
    # Defaults include the standard data-management-frontend dev port (5174)
    # and the chat-frontend dev ports.  In production override this via env var
    # to the Render frontend hostname(s) only.
    cors_origins: list[str] = Field(
        default=[
            "http://localhost:5174",
            "http://localhost:5173",
            "http://localhost:3000",
        ],
        alias="ALLOWED_ORIGINS",
    )


@lru_cache
def get_settings() -> BaseServiceSettings:
    return BaseServiceSettings()
