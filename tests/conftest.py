import pytest  # type: ignore # noqa: F401
import pytest_asyncio
from fastapi import FastAPI, APIRouter
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker

from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.repositories import UserRepository
from app.db.tables.base import BaseTable
from app.models.schemas.user import UserShow, UserRegister
from app.services.auth import create_access_token
from app.api.routes import main_router, science_router, auth_router
from app.main import get_application
from app.db.events import build_engine
from app.db.dumpdata.dump_data import dump_data


@pytest_asyncio.fixture(scope="function")
async def app() -> FastAPI:
    """Get application function"""
    return get_application()


# @pytest_asyncio.fixture(scope='function')
# async def initialized_app(app) -> FastAPI:
#     async with LifespanManager(app) as lifspan:
#         app.state.pool = await build_pool(app, settings=get_app_settings())
#         yield app


@pytest_asyncio.fixture(scope='function')
async def initialized_app(app: FastAPI, settings: AppSettings = get_app_settings()):
    """Initialize application pool and dump data to the database"""
    engine = await build_engine(settings)
    BaseTable.metadata.create_all(bind=engine)
    app.state.pool = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False
    )
    with app.state.pool() as conn:
        try:
            dump_data(conn)
        except Exception:
            pass

    yield app

    BaseTable.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(initialized_app: FastAPI):
    async with AsyncClient(app=initialized_app, base_url="http://localhost:8009") as async_client:
        yield async_client


@pytest_asyncio.fixture(scope='function')
async def session(initialized_app: FastAPI):
    with initialized_app.state.pool() as conn:
        yield conn


@pytest_asyncio.fixture(scope='function')
async def user_data() -> dict:
    return dict(
        username='username',
        password='password',
        email='useremail228@gmail.com',
        first_name='asdasdasf',
        last_name='Poonyl'
    )


@pytest_asyncio.fixture(scope="function")
async def user(user_data: dict, session) -> UserShow:
    user_repo = UserRepository(session)
    new_user = user_repo.create(
        user_schema=UserRegister(**user_data)
    )
    yield new_user.as_dict()
    user_repo.clear()


@pytest_asyncio.fixture(scope="function")
async def token(user: dict) -> str:
    return create_access_token(UserShow(**user).dict())


@pytest_asyncio.fixture(scope="function")
async def authorized_client(token: str, client: AsyncClient) -> AsyncClient:
    client.headers = {
        "Authorization": f"Bearer {token}",
        **client.headers,
    }
    yield client


# comfortable way to test routes
def get_url(router: APIRouter):
    def inner(name: str, **params):
        return router.url_path_for(name, **params)
    return inner


get_main_url = get_url(main_router)
get_auth_url = get_url(auth_router)
get_science_url = get_url(science_router)
