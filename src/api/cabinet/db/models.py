from sqlalchemy import String, Integer, ForeignKey, Column, Float

from infrastructure.db import Base,  TableMixin
from api.auth.db.models import User


class History(Base, TableMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    result = Column(Float)
    user = Column(Integer, ForeignKey("users.id"))
    formula = Column(Integer, ForeignKey("formulas.id"))


