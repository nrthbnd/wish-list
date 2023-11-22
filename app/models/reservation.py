from sqlalchemy import Column, ForeignKey, Integer

from constants import WISH_ID_FOREIGN_KEY
from app.models.custombase import CustomBase


class Reservation(CustomBase):
    """Модель бронирования пожелания."""
    wish_id = Column(
        Integer,
        ForeignKey(WISH_ID_FOREIGN_KEY)
    )
    # user_id = Column(Integer, ForeignKey('user.id'))
