from pydantic import BaseSettings
import logging
import os
from rich.console import Console


class Settings(BaseSettings):
    DB_NAME: str
    DB_PORT: str
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str
    EXPIRES_MINUTES: int

    class Config:
        env_file = '../.dev.env'

GITHUB_REDERECT_URL = "https://github.com/michael7nightingale/Calculations-FastAPI"
def get_settings() -> Settings:
    return Settings()


# logging
def create_logger():
    logger_ = logging.Logger(name='app_loger', level='DEBUG')
    if not os.path.exists(os.getcwd() + '/log/'):
        os.mkdir(os.getcwd() + '/log/')
    file_handler = logging.FileHandler(filename='log/app.log')
    formatter = logging.Formatter("%(asctime)s   |   %(levelname)s   |   %(message)s")
    file_handler.setFormatter(formatter)
    logger_.addHandler(file_handler)
    return logger_


def create_console():
    console_ = Console(highlight=False)
    return console_


logger = create_logger()
console = create_console()

