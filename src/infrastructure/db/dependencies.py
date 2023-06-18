from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from fastapi import Request, Depends

from . import create_pool, create_engine
from .repository import BaseRepository


async def __get_pool(request: Request):
    return request.app.state.pool


async def __get_session(pool: async_sessionmaker = Depends(__get_pool)):
    async with pool() as session:
        yield session


def get_repository(type_: Type[BaseRepository]):

    def inner(session: AsyncSession = Depends(__get_session)):
        return type_(session=session)

    return inner

