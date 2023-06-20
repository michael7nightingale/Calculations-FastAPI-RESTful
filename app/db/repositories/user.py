from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.services.auth import create_uuid
from app.services.hasher import hash_password, verify_password
from app.db.tables.user import User
from app.models.schemas.user import UserLogin, UserRegister
from app.db.repositories.base import BaseRepository
from app.resources.responses import USER_NOT_FOUND, LOGIN_FAIL


class UserRepository(BaseRepository):
    def __init__(self, session: Session):

        super().__init__(model=User, session=session)

    def create(self, user_schema: UserRegister):
        user_schema.password = hash_password(user_schema.password)
        user = super().create(**user_schema.dict())
        return user

    def login(self, user_schema: UserLogin) -> User:
        user = self.get_by(username=user_schema.username)
        if user is None:
            raise HTTPException(detail=USER_NOT_FOUND, status_code=403)
        if verify_password(user_schema.password, user.password):
            return user
        else:
            raise HTTPException(detail=LOGIN_FAIL, status_code=400)
