from .schemas import RequestSchema
from fastapi import Body, Depends
from api.cabinet.db.repository import HistoryRepository
from infrastructure.db.dependencies import get_repository

from formulas import contextBuilder


async def get_result(data: RequestSchema = Body()):
    result = await contextBuilder.build_template(data)
    return result

