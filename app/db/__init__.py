from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base


async def create_engine(dns: str) -> AsyncEngine:
    return create_async_engine(url=dns)


async def create_pool(async_engine: AsyncEngine):
    return async_sessionmaker(bind=async_engine)

