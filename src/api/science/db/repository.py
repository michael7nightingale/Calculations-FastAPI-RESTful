from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from infrastructure.db.repository import BaseRepository, SlugGetMixin
from .models import Formula, Category, Science


class ScienceRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Science, session=session)


class CategoryRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Category, session=session)


class FormulaRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Formula, session=session)
