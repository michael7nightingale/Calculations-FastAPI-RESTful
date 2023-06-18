from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update

from typing import TypeVar


Model = TypeVar("Model")


class BaseRepository:
    def __init__(self, model: Model, session: AsyncSession):
        self._model = model
        self._session = session

    async def get(self, id_):
        query = select(self._model).where(self._model.id == id_)
        return (await self._session.execute(query)).scalar()

    async def all(self):
        query = select(self._model)
        return (await self._session.execute(query)).scalars()

    async def delete(self, id_: int) -> None:
        query = delete(self._model).where(self._model.id == id_)
        await self._session.execute(query)

    async def filter(self, **kwargs):
        conditions = (getattr(self._model, key) == value for key, value in kwargs)
        query = select(self._model).where(*conditions)
        return (await self._session.execute(query)).scalars()

    async def update(self, id_: int, **kwargs):
        query = update(self._model).where(self._model.id == id_).values(**kwargs)
        return (await self._session.execute(query)).scalar()

    async def create(self, **kwargs):
        obj = self._model(**kwargs)
        self._session.add(obj)
        await self._session.commit()
        return obj

    async def commit(self) -> None:
        await self._session.commit()

    async def add(self, obj) -> None:
        self._session.add(obj)


class SlugGetMixin:
    _model: Model
    _session: AsyncSession

    async def get(self, slug: str):
        query = select(self._model).where(self._model.slug == slug)
        return (await self._session.execute(query)).scalar()

