from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.message import MessageResponse


class ChatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        res = v.strip()
        if not res:
            raise ValueError("empty title after stripping")
        return res


class ChatResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    model_config = {"from_attributes": True}


class ChatDetailResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: list["MessageResponse"] = Field(default_factory=list)

    model_config = {"from_attributes": True}
