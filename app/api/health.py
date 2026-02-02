# app/api/health.py
from typing import Dict

from fastapi import APIRouter

from app.core.logging import logger

router = APIRouter()


@router.get("/health", response_model=Dict[str, str])
async def health() -> Dict[str, str]:
    logger.info("Health check request")
    return {"status": "ok"}
