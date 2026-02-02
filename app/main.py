from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import logger, setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.debug("Application is starting up...")
    logger.debug("Swagger UI: http://localhost:8000/docs")
    yield
    logger.debug("Application is shutting down...")


def create_app() -> FastAPI:
    logger.info("Start aplication....")
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="API сервис для управления чатами",
        lifespan=lifespan,
    )
    ##prod
    app.include_router(api_router)
    ##тестовый для првоерки
    app.include_router(health_router)

    logger.debug("Application started!")
    logger.debug("Swagger UI: http://localhost:8000/docs")
    logger.debug("ReDoc: http://localhost:8000/redoc")
    logger.debug("API: http://localhost:8000")
    return app


app: FastAPI = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
