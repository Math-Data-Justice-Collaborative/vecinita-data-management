from pydantic import BaseModel


class PredictRequest(BaseModel):
    text: str
    model_version: str | None = None


class PredictResponse(BaseModel):
    label: str
    score: float
    model_version: str | None = None
