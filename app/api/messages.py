from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import create_message

router = APIRouter(
    tags=["messages"],
)


@router.post(
    "/chats/{chat_id}/messages/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send msg to chat",
)
async def create_message_route(
    chat_id: int,
    message: MessageCreate,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> MessageResponse:
    db_msg = await create_message(db, chat_id, message)
    if db_msg is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id{chat_id} not found",
        )
    return db_msg
