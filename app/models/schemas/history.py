from pydantic import BaseModel
from datetime import datetime


class HistoryIn(BaseModel):
    user: str
    result: str
    formula: str


class HistoryOut(BaseModel):
    result: str
    formula: str
    date_time: datetime
