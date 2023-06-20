from app.core.settings.app import AppSettings


class ProductionAppSettings(AppSettings):
    class Config(AppSettings.Config):
        env_file = 'prod.env'
