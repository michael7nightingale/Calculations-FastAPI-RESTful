from sqlalchemy import Column, String, Integer, Text

from infrastructure.db import Base, TableMixin


class Science(Base, TableMixin):
    __tablename__ = 'sciences'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(40), unique=True)
    content = Column(Text)
    slug = Column(String(40), unique=True)


class Category(Base, TableMixin):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(40), unique=True)
    content = Column(Text)
    super_category = Column(String(40))
    slug = Column(String(40), unique=True)


class Formula(Base, TableMixin):
    __tablename__ = 'formulas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(40), unique=True)
    formula = Column(String(40))
    content = Column(Text)
    category_id = Column(Integer)
    slug = Column(String(40), unique=True)
