from fastapi import FastAPI

from app.core.settings.app import AppSettings
from app.db.events import build_pool, close_pool


def startup_app_handler(
        app: FastAPI,
        settings: AppSettings
):
    async def startup_app() -> None:
        await build_pool(app, settings)

    return startup_app


def shutdown_app_handler(app: FastAPI):

    async def shutdown_app():
        await close_pool(app)

    return shutdown_app
