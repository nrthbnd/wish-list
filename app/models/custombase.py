from sqlalchemy import Column, DateTime, Text

from constants import (
    CREATE_DATE_DEFAULT, CLOSE_DATE_DEFAULT,
)
from app.core.db import Base


class CustomBase(Base):
    """Абстрактный базовый класс для модели Wish и Reservation."""
    __abstract__ = True

    comment = Column(Text)
    create_date = Column(DateTime, default=CREATE_DATE_DEFAULT)
    close_date = Column(DateTime, default=CLOSE_DATE_DEFAULT)
