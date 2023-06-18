from pydantic import BaseModel
from enum import Enum


class ScienceEnum(str, Enum):
    physics = 'physics'
    mathem = 'mathem'


class RequestSchema(BaseModel):
    method: str
    formula_slug: str
    url: str
    user_id: int| None = None
    data: dict | None = None
    nums_comma: int | None = None
    find_mark: str | None = None


