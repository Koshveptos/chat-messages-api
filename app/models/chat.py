import time

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[float] = mapped_column(
        Float, default=lambda: time.time(), nullable=False
    )
    messages: Mapped[list["Message"]] = relationship(  # noqa: F821
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Message.created_at.desc()",
    )

    def __repr__(self) -> str:
        return f"Chat(id={self.id} , title = {self.title})"
