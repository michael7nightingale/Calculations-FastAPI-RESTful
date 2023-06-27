from fastapi import Depends, Body
from fastapi.security import OAuth2PasswordBearer
from starlette.exceptions import HTTPException

from app.models.schemas.user import UserLogin, UserShow
from app.api.dependencies.database import get_repository
from app.db.repositories.user import UserRepository
from app.services.auth import create_access_token, decode_access_token
from app.resources.responses import NO_PERMISSIONS


oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: str = Depends(oauth_scheme)) -> UserShow:
    user_data = decode_access_token(token)
    return UserShow(**user_data)


async def get_superuser(user: UserShow = Depends(get_current_user)) -> UserShow:
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail=NO_PERMISSIONS)
    return user


async def get_login_user(user_schema: UserLogin = Body(),
                         user_repo: UserRepository = Depends(get_repository(UserRepository))) -> dict:
    user = user_repo.login(user_schema)
    return UserShow(**user.as_dict()).dict()


async def get_token_(user: dict = Depends(get_login_user)) -> str:
    token = create_access_token(user)
    return token
