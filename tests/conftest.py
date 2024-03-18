from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# from app.core.db import Base

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

try:
    from app.main import app  # noqa
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект приложения `app`. '
        'Проверьте и поправьте: он должен быть доступен в модуле `app.main`.',
    )

try:
    from app.core.db import Base  # noqa
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект `Base`. '
        'Проверьте и поправьте: они должны быть доступны в модуле '
        '`app.core.db`.',
    )

DB_USER = "test_postgres"
DB_PASS = "test_postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "test_wish-list_db"


# Создаем фикстуру для настройки тестовой базы данных и сессии
@pytest.fixture
async def init_db():
    engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(init_db):
    session = sessionmaker(init_db, class_=AsyncSession, expire_on_commit=False)
    async with session() as s:
        yield s
