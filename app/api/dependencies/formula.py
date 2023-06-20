from fastapi import Body, Depends

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_repository
from app.db.repositories import HistoryRepository
from app.models.schemas.science import RequestSchema
from app.formulas import contextBuilder


async def get_result(data: RequestSchema = Body(),
                     user = Depends(get_current_user),
                     history_repo: HistoryRepository = Depends(get_repository(HistoryRepository))):
    data.user_id = user.id
    result = contextBuilder.build_template(request=data, history_repo=history_repo)
    return result

