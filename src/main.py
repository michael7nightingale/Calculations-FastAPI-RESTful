from fastapi import FastAPI
import uvicorn

from api.auth.routes import auth_router
from api.main.routes import main_router
from infrastructure.db import create_engine, create_pool
from sqlalchemy import create_engine
from config import get_settings


def create_app() -> FastAPI:

    app_ = FastAPI()

    routers = (main_router, auth_router)
    for router in routers:
        app_.include_router(router=router)

    settings = get_settings()

    @app.on_event("startup")
    async def on_startup():
        engine = await create_engine(
            dns=f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
        )
        app_.state.pool = await create_pool(engine)

    return app_


app = create_app()


if __name__ == '__main__':
    uvicorn.run(
        reload=True,
        app="main:app",
        host="localhost",
        port=8000,

    )
