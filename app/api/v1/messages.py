from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter(
    tags=["messages"],
)


@router.post(
    "/chats/{chat_id}/messages/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send msg to chat",
)
async def create_message(
    chat_id: int,
    message: MessageCreate,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> MessageResponse:
    chat: Chat | None = await db.get(Chat, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id{chat_id} not found",
        )

    db_msg = Message(chat_id=chat_id, text=message.text)
    db.add(db_msg)
    await db.commit()
    await db.refresh(db_msg)
    return db_msg
