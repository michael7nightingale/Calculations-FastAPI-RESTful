import logging
from typing import Any

from pydantic import PostgresDsn, SecretStr

from app.core.settings.base import BaseSettings
from fastapi import FastAPI


class AppSettings(BaseSettings):
    debug: bool = True
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Calculations"
    version: str = '1.0'

    database_url: PostgresDsn
    max_connection_count: int = 100
    min_connection_count: int = 1

    secret_key: SecretStr
    algorithm: str = "HS256"

    api_prefix: str = "/api"

    jwt_token_prefix: str = "Token"

    allowed_hosts: list[str] = ['*']

    logging_level: int = logging.INFO
    loggers: list = []

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version

        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = []
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = []


