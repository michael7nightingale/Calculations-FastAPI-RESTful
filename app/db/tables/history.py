from sqlalchemy import String, DateTime, Integer, ForeignKey, Float, func
from sqlalchemy.orm import mapped_column
from app.db.tables.base import BaseTable, TableMixin, UUIDPrimaryKey


class History(UUIDPrimaryKey, BaseTable, TableMixin):
    __tablename__ = 'history'

    result = mapped_column(Float)
    user = mapped_column(String, ForeignKey("user.id"))
    formula = mapped_column(Integer, ForeignKey("formula.title"))
    date_time = mapped_column(DateTime(timezone=True), server_default=func.now())
