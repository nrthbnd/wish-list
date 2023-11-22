from sqlalchemy import Boolean, Column, String

from constants import (
    COMPLETED_DEFAULT,
    RESERVED_DEFAULT,
    WISH_NAME_MAX_LEN,
)
from app.models.custombase import CustomBase


class Wish(CustomBase):
    """Модель пожелания."""
    name = Column(
        String(WISH_NAME_MAX_LEN),
        unique=True,
        nullable=False,
    )
    completed = Column(
        Boolean,
        default=COMPLETED_DEFAULT,
    )
    reserved = Column(
        Boolean,
        default=RESERVED_DEFAULT,
    )
