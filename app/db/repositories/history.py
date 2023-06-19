from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository
from app.db.tables.history import History


class HistoryRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=History)

    async def create(self, history_scheme):
        new_history = super().create(**history_scheme.dict())
        return new_history
