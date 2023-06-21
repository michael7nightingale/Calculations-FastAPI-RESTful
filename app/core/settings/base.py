from enum import Enum
from pydantic import BaseSettings


class AppEnvTypes(str, Enum):
    prod = "prod"
    dev = "dev"
    test = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.test

