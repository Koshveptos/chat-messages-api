from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class MessageCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

    @field_validator("text")
    @classmethod
    def strip_text(cls, v: str) -> str:
        res = v.strip()
        if not res:
            raise ValueError("empty title after stripping")
        return res


class MessageResponse(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}
