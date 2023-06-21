from fastapi import APIRouter, Depends
from starlette.responses import FileResponse
from starlette.exceptions import HTTPException

from app.resources.responses import HISTORY_DOWNLOAD_ERROR
from app.api.dependencies import get_user_history, get_history_file
from app.models.schemas import HistoryOut


cabinet_router = APIRouter(prefix="/cabinet")


@cabinet_router.get('/history', response_model=list[HistoryOut])
async def get_history(history=Depends(get_user_history)):
    return (h.as_dict() for h in history)


@cabinet_router.post('/history/download')
async def download_history(filepath: str = Depends(get_history_file)):
    if filepath is None:
        raise HTTPException(status_code=500, detail=HISTORY_DOWNLOAD_ERROR)
    return FileResponse(path=filepath)

