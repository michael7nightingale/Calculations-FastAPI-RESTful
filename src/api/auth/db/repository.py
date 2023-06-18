from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.utils.auth import create_uuid
from infrastructure.utils.hasher import hash_password, verify_password

from .models import User
from ..schemas import UserLogin, UserRegister
from infrastructure.db.repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):

        super().__init__(model=User, session=session)

    async def create(self, user_schema: UserRegister):
        user = self._model(
            id=create_uuid(),
            username=user_schema.username,
            password=hash_password(user_schema.password),
            email=user_schema.email,
            first_name=user_schema.first_name,
            last_name=user_schema.last_name
        )
        await self.add(user)
        await self.commit()
        return user

    async def login(self, user_schema: UserLogin) -> User:
        user = await self.filter(username=user_schema.username)
        if verify_password(user_schema.password, user.password):
            return user
        else:
            raise ValueError
