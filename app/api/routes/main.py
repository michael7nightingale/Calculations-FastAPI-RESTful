from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from ..dependencies.auth import get_superuser
from app.models.schemas.user import UserShow
from app.db.dumpdata.dump_data import dump_data
from ..dependencies.database import __get_session

main_router = APIRouter(prefix='', tags=['Main'])


@main_router.get("/")
async def homepage(request: Request):
    """Главная страница"""
    return {"message": "This is main page"}


@main_router.post("/dump-data")
async def dump_data_view(superuser: UserShow = Depends(get_superuser),
                         session: Session = Depends(__get_session)):
    try:
        dump_data(session)
        return {"detail": "Data dumped successfully"}
    except Exception as e:
        return {"error": str(e)}
