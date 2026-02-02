from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.message import MessageCreate


async def create_message(
    db: AsyncSession, chat_id: int, message_data: MessageCreate
) -> Message | None:
    logger.debug(
        f"Servise: create msg in chat  ID = {chat_id}"
        f" with len = {len(message_data.text)}"
    )
    chat: Chat | None = await db.get(Chat, chat_id)
    if chat is None:
        logger.warning(f"Servise: Chat with ID = {chat_id} not fount")
        return None
    db_msg = Message(chat_id=chat_id, text=message_data.text)
    db.add(db_msg)
    await db.commit()
    await db.refresh(db_msg)
    logger.debug(
        f"Servise: seccessfully create msg in chat ID = {chat_id}"
        f" with len = {len(message_data.text)}"
    )
    return db_msg
