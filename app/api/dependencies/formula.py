from fastapi import Body, Depends

from app.models.schemas.science import RequestSchema
from app.formulas import contextBuilder


async def get_result(data: RequestSchema = Body()):
    result = await contextBuilder.build_template(data)
    return result

