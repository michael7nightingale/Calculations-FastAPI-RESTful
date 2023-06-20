from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, update

from typing import TypeVar

from app.services.auth import create_uuid

Model = TypeVar("Model")


class BaseRepository:
    def __init__(self, model: Model, session: Session):
        self._model = model
        self._session = session

    def get(self, id_):
        query = select(self._model).where(self._model.id == id_)
        return (self._session.execute(query)).scalar_one_or_none()

    def all(self):
        query = select(self._model)
        return (self._session.execute(query)).scalars().all()

    def delete(self, id_: int) -> None:
        query = delete(self._model).where(self._model.id == id_)
        self._session.execute(query)

    def filter(self, **kwargs):
        query = select(self._model).filter_by(**kwargs)
        return (self._session.execute(query)).scalars().all()

    def get_by(self, **kwargs):
        query = select(self._model).filter_by(**kwargs)
        return (self._session.execute(query)).scalar_one_or_none()

    def update(self, id_: int, **kwargs):
        query = update(self._model).where(self._model.id == id_).values(**kwargs)
        return (self._session.execute(query)).scalar_one_or_none()

    def create(self, **kwargs):
        obj = self._model(**kwargs)
        self.save(obj)
        return obj

    def save(self, obj: Model):
        self.add(obj)
        self._session.commit()

    def commit(self) -> None:
        self._session.commit()

    def add(self, obj) -> None:
        self._session.add(obj)


class SlugGetMixin:
    _model: Model
    _session: Session

    def get(self, slug: str):
        query = select(self._model).where(self._model.slug == slug)
        return (self._session.execute(query)).scalar_one_or_none()

