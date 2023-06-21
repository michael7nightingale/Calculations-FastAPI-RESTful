from fastapi import Depends
import os

from app.api.dependencies.auth import get_current_user
from app.models.schemas import UserShow
from app.api.dependencies.database import get_repository
from app.db.repositories import HistoryRepository

from app.services.tables.tables import CsvTableManager


async def get_user_history(
        user: UserShow = Depends(get_current_user),
        history_repo: HistoryRepository = Depends(get_repository(HistoryRepository))
):
    history = history_repo.filter(user=user.id)
    return history


async def get_history_file(
    user: UserShow = Depends(get_current_user),
    history_repo: HistoryRepository = Depends(get_repository(HistoryRepository))
):
    filepath = f"files/tables/{user.id}.csv"
    history = history_repo.filter(user=user.id)
    table = CsvTableManager(filepath=filepath)
    if history:
        test_column: dict = history[0].as_dict()
        table.init_data(test_column.keys())
        for h in history:
            table.add_line_dict(h.as_dict())
        table.save_data()
        yield filepath
        os.remove(filepath)     # deleting file after response
    else:
        yield None
