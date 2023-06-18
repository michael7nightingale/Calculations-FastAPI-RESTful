from jose import JWTError, jwt
from starlette.exceptions import HTTPException
from uuid import uuid4

from config import get_settings


def create_access_token(data) -> str:
    settings = get_settings()
    token = jwt.encode(
        claims=data,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token


def decode_access_token(token) -> dict:
    try:
        settings = get_settings()
        data = jwt.decode(
            token=token ,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return data
    except JWTError:
        raise HTTPException(status_code=403)


def create_uuid() -> str:
    return str(uuid4())
