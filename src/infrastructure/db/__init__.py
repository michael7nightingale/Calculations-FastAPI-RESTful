from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base


async def create_engine(dns: str) -> AsyncEngine:
    with create_async_engine(url=dns) as async_engine:
        yield async_engine


async def create_pool(async_engine: AsyncEngine):
    with async_sessionmaker(bind=async_engine) as async_pool:
        yield async_pool


class TableMixin:
    __table__: str

    def as_dict(self) -> dict:
        return {i.name: getattr(self, i.name) for i in self.__table__.columns}


Base = declarative_base()
