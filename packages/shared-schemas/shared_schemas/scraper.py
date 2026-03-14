from pydantic import BaseModel, Field, HttpUrl


class ScrapeRequest(BaseModel):
    url: HttpUrl
    depth: int = 1


class ScrapeResult(BaseModel):
    url: str
    title: str | None = None
    text: str | None = None
    metadata: dict = Field(default_factory=dict)
