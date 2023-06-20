from sqlalchemy.exc import InvalidRequestError, IntegrityError
from sqlalchemy.ext.asyncio import (async_sessionmaker, create_async_engine,
                                    AsyncEngine, AsyncSession)
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
from .tables import User
from fastapi import Depends, FastAPI

from app.core.settings.app import AppSettings
from ..services.hasher import hash_password


async def build_engine(settings: AppSettings):
    return create_engine(url=settings.database_url)


async def build_pool(app: FastAPI, settings: AppSettings) -> None:
    engine = await build_engine(settings)

    app.state.pool = sessionmaker(
        expire_on_commit=False,
        autoflush=False,
        bind=engine

    )


async def close_pool(app: FastAPI) -> None:
    app.state.pool.close()


async def create_superuser(app, settings: AppSettings):
    with app.state.pool() as session:
        try:
            superuser = User(
                **settings.superuser_kwargs,
                is_superuser=True,
                is_staff=True
            )
            session.add(superuser)
            session.commit()
        except IntegrityError:
            session.rollback()
            data = settings.superuser_kwargs
            data['password'] = hash_password(data['password'])
            session.execute(
                update(User).where(User.username == settings.superuser_username).values(
                    **data,
                    is_superuser=True,
                    is_staff=True
                )
            )
            session.commit()

