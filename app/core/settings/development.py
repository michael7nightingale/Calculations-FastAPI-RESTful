import logging

from app.core.settings.app import AppSettings


class DevelopmentAppSettings(AppSettings):
    debug: bool = True

    logging_level = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = 'dev.env'
