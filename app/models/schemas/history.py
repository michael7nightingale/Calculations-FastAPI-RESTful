from pydantic import BaseModel


class HistorySchema(BaseModel):
    user_id: int
    result: str
    formula: str
    formula_url: str
    date_time: str
