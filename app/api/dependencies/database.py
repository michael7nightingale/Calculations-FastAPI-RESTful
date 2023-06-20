from typing import Type
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Request, Depends

from app.db.repositories.base import BaseRepository


async def __get_pool(request: Request):
    return request.app.state.pool


async def __get_session(pool: sessionmaker = Depends(__get_pool)):
    with pool() as session:
        yield session


def get_repository(type_: Type[BaseRepository]):

    def inner(session: Session = Depends(__get_session)):
        return type_(session=session)

    return inner


