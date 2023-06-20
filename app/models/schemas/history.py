from pydantic import BaseModel


class HistorySchema(BaseModel):
    user: str
    result: str
    formula: str
