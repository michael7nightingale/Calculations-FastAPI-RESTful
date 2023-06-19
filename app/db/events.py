from sqlalchemy.ext.asyncio import (async_sessionmaker, create_async_engine,
                                    AsyncEngine, AsyncSession)
from fastapi import Depends, FastAPI

from app.core.settings.app import AppSettings


async def build_engine(settings: AppSettings):
    return create_async_engine(url=settings.database_url)


async def build_pool(app: FastAPI, settings: AppSettings) -> None:
    engine = await build_engine(settings)

    app.state.pool = async_sessionmaker(
        expire_on_commit=False,
        autoflush=False,
        bind=engine

    )


async def close_pool(app: FastAPI) -> None:
    app.state.pool.close()


