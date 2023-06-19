from sqlalchemy import (String, DateTime,
                        Boolean, Integer, Text, ForeignKey)
from sqlalchemy.orm import mapped_column
from app.db.tables.base import BaseTable, TableMixin, IDPrimaryKey


class Formula(IDPrimaryKey, BaseTable, TableMixin):
    __tablename__ = 'formula'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(40), unique=True)
    formula = mapped_column(String(40))
    content = mapped_column(Text)
    category = mapped_column(String(40), ForeignKey("category.title"))
    slug = mapped_column(String(40), unique=True)
