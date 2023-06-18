from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.repository import BaseRepository
from .models import History


class HistoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=History)

    async def create(self, history_scheme):
        new_history = self._model(**history_scheme.dict())
        self.add(new_history)
        await self.commit()