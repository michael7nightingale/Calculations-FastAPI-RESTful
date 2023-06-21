from jose import JWTError, jwt
from starlette.exceptions import HTTPException
from uuid import uuid4

from app.core.config import get_app_settings


def create_access_token(data: dict) -> str:
    settings = get_app_settings()
    token = jwt.encode(
        claims=data,
        key=str(settings.secret_key),
        algorithm=settings.algorithm
    )
    return token


def decode_access_token(token: str) -> dict:
    try:
        settings = get_app_settings()
        data = jwt.decode(
            token=token,
            key=str(settings.secret_key),
            algorithms=[settings.algorithm]
        )
        return data
    except JWTError:
        raise HTTPException(status_code=403)


def create_uuid() -> str:
    return str(uuid4())
