from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import logger


def create_app() -> FastAPI:
    logger.info("Start aplication....")
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="API сервис для управления чатами и приложениями",
    )
    ##prod
    app.include_router(api_router)
    ##тестовый для првоерки
    app.include_router(health_router)
    return app


app: FastAPI = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port="8000",
        reload=True,
    )
