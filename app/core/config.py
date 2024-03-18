from pydantic import BaseSettings

from constants import (
    APP_TITLE, SECRET, ENV_FILE_NAME,
)


class Settings(BaseSettings):
    """Считывать переменные окружения из файла."""
    app_title: str = APP_TITLE
    secret: str = SECRET
    database_url: str

    class Config:
        """Файл с переменными окружения."""
        env_file = ENV_FILE_NAME


settings = Settings()
