from sqlalchemy import String, Text
from sqlalchemy.orm import mapped_column
from app.db.tables.base import BaseTable, TableMixin, IDPrimaryKey


class Science(IDPrimaryKey, BaseTable, TableMixin):
    __tablename__ = 'science'

    title = mapped_column(String(40), unique=True)
    content = mapped_column(Text)
    slug = mapped_column(String(40), unique=True)
