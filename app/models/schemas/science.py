from pydantic import BaseModel
from enum import Enum


class ScienceEnum(str, Enum):
    physics = 'physics'
    mathem = 'mathem'


class ScienceShow(BaseModel):
    id: str
    title: str
    content: str


class CategoryShow(BaseModel):
    id: int
    title: str
    content: str
    science: str


class FormulaShow(BaseModel):
    title: str
    formula: str
    content: str
    category: str


class RequestSchema(BaseModel):
    formula_slug: str
    data: dict
    find_mark: str
    user_id: str | None = None
    nums_comma: int | None = 10
