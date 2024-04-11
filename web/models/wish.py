from sqlalchemy import Boolean, Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from constants import (
    COMPLETED_DEFAULT,
    RESERVED_DEFAULT,
    WISH_NAME_MAX_LEN,
    LINK_URL_MAX_LEN,
    LINK_URL_DEFAULT,
)
from models.custombase import CustomBase


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
    wish_link = Column(
        String(LINK_URL_MAX_LEN),
        nullable=True,
        default=LINK_URL_DEFAULT,
    )
    reservation = relationship('Reservation', cascade='delete')
    user_id = Column(Integer, ForeignKey('user.id'))
