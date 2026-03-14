from pydantic import BaseModel


class EmbedRequest(BaseModel):
    text: str
    model_version: str | None = None


class EmbedResponse(BaseModel):
    embedding: list[float]
    model_version: str | None = None
