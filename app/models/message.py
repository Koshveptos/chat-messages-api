import time

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    text: Mapped[str] = mapped_column(String(5000), nullable=False)
    created_at: Mapped[float] = mapped_column(
        Float, default=lambda: time.time(), nullable=False
    )
    chat: Mapped["Chat"] = relationship(  # noqa: F821
        "Chat", back_populates="messages", lazy="joined"
    )

    def __repr__(self) -> str:
        return f"Message (id = {self.id}, chat_id = {self.chat_id}, text={self.text})"
