from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from .tables import User
from fastapi import FastAPI

from app.core.settings.app import AppSettings
from ..services.hasher import hash_password


async def build_engine(settings: AppSettings):
    return create_engine(url=settings.database_url)


async def build_pool(app: FastAPI, settings: AppSettings) -> None:
    engine = await build_engine(settings)

    app.state.pool = sessionmaker(
        expire_on_commit=False,
        autoflush=False,
        bind=engine

    )


async def close_pool(app: FastAPI) -> None:
    app.state.pool.close_all()


async def create_superuser(app, settings: AppSettings):
    with app.state.pool() as session:
        data = settings.superuser_kwargs
        data['password'] = hash_password(data['password'])
        try:
            superuser = User(
                **data,
                is_superuser=True,
                is_staff=True
            )
            session.add(superuser)
            session.commit()
        except IntegrityError:
            session.rollback()
            session.execute(
                update(User).where(User.username == settings.superuser_username).values(
                    **data,
                    is_superuser=True,
                    is_staff=True
                )
            )
            session.commit()
