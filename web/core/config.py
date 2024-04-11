import os
from typing import Optional
from pydantic import BaseSettings, EmailStr
from dotenv import load_dotenv

from constants import APP_TITLE, ENV_FILE_NAME

load_dotenv()


class Settings(BaseSettings):
    """Считывать переменные окружения из файла."""
    app_title: str = APP_TITLE
    secret: str = os.getenv('SECRET')
    database_url: str
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        """Файл с переменными окружения."""
        env_file = ENV_FILE_NAME


settings = Settings()
