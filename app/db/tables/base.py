from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, UUID, func, String

from app.services.auth import create_uuid


class BaseTable(DeclarativeBase):
    pass


class UUIDPrimaryKey:
    id = mapped_column(String(80), primary_key=True, default=create_uuid)


class IDPrimaryKey:
    id = mapped_column(Integer, primary_key=True, autoincrement=True)


class TableMixin:
    __table__: str

    def as_dict(self) -> dict:
        return {i.name: getattr(self, i.name) for i in self.__table__.columns}
