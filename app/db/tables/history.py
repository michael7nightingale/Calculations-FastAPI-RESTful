from sqlalchemy import (Column, String, DateTime,
                        Boolean, UUID, Integer, ForeignKey,
                        Float)
from sqlalchemy.orm import mapped_column
from app.db.tables.base import BaseTable, TableMixin, UUIDPrimaryKey


class History(UUIDPrimaryKey, BaseTable, TableMixin):
    __tablename__ = 'history'

    result = mapped_column(Float)
    user = mapped_column(UUID, ForeignKey("user.id"))
    formula = mapped_column(Integer, ForeignKey("formula.title"))
