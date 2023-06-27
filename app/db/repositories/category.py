from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository, SlugGetMixin

from app.db.tables.category import Category


class CategoryRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: Session):
        super().__init__(model=Category, session=session)
