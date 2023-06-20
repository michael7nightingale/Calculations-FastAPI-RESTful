from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository, SlugGetMixin
from app.db.tables.science import Science


class ScienceRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: Session):
        super().__init__(model=Science, session=session)
