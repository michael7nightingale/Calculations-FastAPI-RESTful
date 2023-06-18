from fastapi import APIRouter, Depends, Body
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from config import GITHUB_REDERECT_URL
from .schemas import UserLogin, UserShow, UserRegister
from .db.repository import UserRepository
from infrastructure.db.dependencies import get_repository
from .dependencies import get_token_, get_current_user


auth_router = APIRouter(prefix='/auth')


@auth_router.post("/token")
async def get_token(token: str = Depends(get_token_)):
    return {"access_token": token}


@auth_router.post("/register")
async def register_user(user_repo: UserRepository = Depends(get_repository(UserRepository)),
                        user_schema: UserRegister = Body()):
    try:
        user = await user_repo.create(user_schema)
        return user.as_dict()
    except (IntegrityError, PendingRollbackError):
        raise HTTPException(status_code=403, detail="asondo")


@auth_router.get("/github/")
async def github_redirect():
    return RedirectResponse(
        url=GITHUB_REDERECT_URL,
        status_code=303,

    )
