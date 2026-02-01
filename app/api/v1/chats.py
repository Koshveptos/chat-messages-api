from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.chat import ChatCreate, ChatDetailResponse, ChatResponse

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post(
    "/",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Created new chat",
)
async def create_chat(
    chat_data: ChatCreate, db: Annotated[AsyncSession, Depends(get_db_session)]
) -> ChatResponse:
    db_chat = Chat(title=chat_data.title)
    db.add(db_chat)
    await db.commit()
    await db.refresh(db_chat)
    return db_chat


@router.get(
    "/{chat_id}",
    response_model=ChatDetailResponse,
    summary="Get chat by id",
)
async def get_chat(
    chat_id: int,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="defount = 20 max = 100",
        ),
    ] = 20,
) -> ChatDetailResponse:
    chat: Chat | None = await db.get(Chat, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found",
        )
    print(f"Chat ID: {chat_id}, Chat: {chat}")
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    messages = list(result.scalars().all())
    print(f"Messages found: {len(messages)}")
    chat.messages = messages
    return chat


@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="delete chat",
)
async def delete_chat(
    chat_id: int, db: Annotated[AsyncSession, Depends(get_db_session)]
) -> None:
    chat: Chat | None = await db.get(Chat, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found",
        )
    await db.delete(chat)
    await db.commit()
    return None
