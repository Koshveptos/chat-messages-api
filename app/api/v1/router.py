from fastapi import APIRouter

from app.api.v1 import chats, messages

api_router = APIRouter()

api_router.include_router(chats.router)
api_router.include_router(messages.router)
