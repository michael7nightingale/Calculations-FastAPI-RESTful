from sqlalchemy import String, DateTime, Boolean, func
from sqlalchemy.orm import mapped_column

from app.db.tables.base import BaseTable, TableMixin, UUIDPrimaryKey


class User(UUIDPrimaryKey, BaseTable, TableMixin):
    __tablename__ = 'user'

    username = mapped_column(String(40), unique=True)
    first_name = mapped_column(String(40))
    last_name = mapped_column(String(40), nullable=True)
    email = mapped_column(String(50), unique=True)
    password = mapped_column(String(200))
    last_login = mapped_column(DateTime(timezone=True), server_default=func.now())
    date_join = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_superuser = mapped_column(Boolean, default=False)
    is_staff = mapped_column(Boolean, default=False)
