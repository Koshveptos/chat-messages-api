from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.chat import ChatCreate


async def create_chat(db: AsyncSession, chat_data: ChatCreate) -> Chat:
    logger.debug(f"Servise: Create chat with title{chat_data.title}")
    db_chat = Chat(title=chat_data.title)
    db.add(db_chat)
    await db.commit()
    await db.refresh(db_chat)
    logger.debug(
        f"Servide: Seccesfuully create chat with ID = {db_chat.id}"
        f" title = {chat_data.title}"
    )
    return db_chat


async def get_chat(db: AsyncSession, chat_id: int, limit: int = 20) -> Chat | None:
    logger.debug(f"Servis: Get chat ID = {chat_id} with limit = {limit}")
    chat: Chat | None = await db.get(Chat, chat_id)
    if chat is None:
        logger.warning(f"Servis: Chat with ID = {chat_id} not found")
        return None
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    chat.messages = list(result.scalars().all())
    logger.debug(
        f"Servis: Seccessfully get chat ID = {chat_id}"
        f" with {len(chat.messages)} messages "
    )
    return chat


async def delete_chat(db: AsyncSession, chat_id: int) -> bool | None:
    logger.debug(f"Servise: delit chat ID = {chat_id}")
    chat: Chat | None = await db.get(Chat, chat_id)
    if chat is None:
        logger.warning(f"Servis: Chat with ID = {chat_id} not found")
        return None
    await db.delete(chat)
    await db.commit()
    logger.debug(f"Servise: secceessfully deleted chat ID = {chat_id}")
    return True
