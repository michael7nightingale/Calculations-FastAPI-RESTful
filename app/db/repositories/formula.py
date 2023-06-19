from app.db.repositories.base import BaseRepository, SlugGetMixin
from app.db.tables.formula import Formula

from sqlalchemy.orm import Session


class FormulaRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: Session):
        super().__init__(model=Formula, session=session)
