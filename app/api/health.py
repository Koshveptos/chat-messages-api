# app/api/health.py
from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", response_model=Dict[str, str])
async def health() -> Dict[str, str]:
    return {"status": "ok"}
