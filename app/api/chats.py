from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.chat import ChatCreate, ChatDetailResponse, ChatResponse
from app.services.chat_service import create_chat, delete_chat, get_chat

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post(
    "/",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Created new chat",
)
async def create_chat_route(
    chat_data: ChatCreate, db: Annotated[AsyncSession, Depends(get_db_session)]
) -> ChatResponse:
    db_chat = await create_chat(db, chat_data)
    return db_chat


@router.get(
    "/{chat_id}",
    response_model=ChatDetailResponse,
    summary="Get chat by id",
)
async def get_chat_route(
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
    chat = await get_chat(db, chat_id, limit)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found",
        )
    return chat


@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="delete chat",
)
async def delete_chat_route(
    chat_id: int, db: Annotated[AsyncSession, Depends(get_db_session)]
) -> None:
    chat = await delete_chat(db, chat_id)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found",
        )
    return None
