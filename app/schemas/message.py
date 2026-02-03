from datetime import datetime

from pydantic import BaseModel, Field, field_serializer, field_validator


class MessageCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

    @field_validator("text")
    @classmethod
    def strip_text(cls, v: str) -> str:
        res = v.strip()
        if not res:
            raise ValueError("empty text after stripping")
        return res


class MessageResponse(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: float

    @field_serializer("created_at")
    def seriaze_created_at(self, created_at: float) -> str:
        return datetime.fromtimestamp(created_at).isoformat()

    model_config = {"from_attributes": True}
