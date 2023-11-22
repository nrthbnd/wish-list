from pydantic import BaseSettings

from constants import (
    APP_TITLE, DATABASE_URL, SECRET, ENV_FILE_NAME,
)


class Settings(BaseSettings):
    """Считывать переменные окружения из файла."""
    app_title: str = APP_TITLE
    database_url: str = DATABASE_URL
    secret: str = SECRET

    class Config:
        """Файл с переменными окружения."""
        env_file = ENV_FILE_NAME


settings = Settings()
