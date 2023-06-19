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
    method: str
    formula_slug: str
    url: str
    user_id: int| None = None
    data: dict | None = None
    nums_comma: int | None = None
    find_mark: str | None = None


