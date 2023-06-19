from sqlalchemy.orm import Session

from app.services.auth import create_uuid
from app.services.hasher import hash_password, verify_password
from app.db.tables.user import User
from app.models.schemas.user import UserLogin, UserRegister
from app.db.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: Session):

        super().__init__(model=User, session=session)

    async def create(self, user_schema: UserRegister):
        user = super().create(**user_schema.dict())
        return user

    async def login(self, user_schema: UserLogin) -> User:
        user = await self.filter(username=user_schema.username)
        if verify_password(user_schema.password, user.password):
            return user
        else:
            raise ValueError
