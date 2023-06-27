import logging

from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True

    secret_key: str = "12094joqsfnalfsmas[ori"

    database_url: str

    max_connection_count = 5
    min_connection_count = 5

    logging_level = logging.DEBUG

    class Config:
        env_file = "test.env"
