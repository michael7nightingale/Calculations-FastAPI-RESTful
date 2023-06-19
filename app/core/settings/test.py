import logging

from pydantic import SecretStr, PostgresDsn

from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True

    secret_key: SecretStr = SecretStr("test_+apapsd")

    database_url: PostgresDsn

    max_connection_count = 5
    min_connection_count = 5

    logging_level = logging.DEBUG
