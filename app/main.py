from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from app.core.config import get_app_settings
from app.core.events import shutdown_app_handler, startup_app_handler


def get_application() -> FastAPI:
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts
    )

    application.add_event_handler(
        'startup',
        startup_app_handler(application, settings)
    )

    application.add_event_handler(
        "shutdown",
        shutdown_app_handler(application)
    )

    routers = ()

    for router in routers:
        application.include_router(router)

    return application


app = get_application()
