from sqlalchemy import (Column, String, DateTime,
                        Boolean, Integer, Text, ForeignKey)
from sqlalchemy.orm import mapped_column
from app.db.tables.base import BaseTable, TableMixin, IDPrimaryKey


class Category(IDPrimaryKey, BaseTable, TableMixin):
    __tablename__ = 'category'

    title = mapped_column(String(40), unique=True)
    content = mapped_column(Text)
    science = mapped_column(String(40), ForeignKey("science.title"))
    slug = mapped_column(String(40), unique=True)
