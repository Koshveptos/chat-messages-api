from datetime import datetime

from pydantic import BaseModel, Field, field_serializer, field_validator

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
    created_at: float

    @field_serializer("created_at")
    def seriaze_created_at(self, created_at: float) -> str:
        return datetime.fromtimestamp(created_at).isoformat()

    model_config = {"from_attributes": True}


class ChatDetailResponse(BaseModel):
    id: int
    title: str
    created_at: float
    messages: list["MessageResponse"] = Field(default_factory=list)

    model_config = {"from_attributes": True}
