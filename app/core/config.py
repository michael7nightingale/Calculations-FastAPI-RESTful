from typing import Type

from app.core.settings.app import AppSettings
from app.core.settings.base import BaseAppSettings, AppEnvTypes
from app.core.settings.production import ProductionAppSettings
from app.core.settings.test import TestAppSettings
from app.core.settings.development import DevelopmentAppSettings


environments: dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevelopmentAppSettings,
    AppEnvTypes.prod: ProductionAppSettings,
    AppEnvTypes.test: TestAppSettings
}


def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
