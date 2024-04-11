from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Extra, Field

from constants import COMMENT_MIN_LEN, CREATE_DATE


class ReservationBase(BaseModel):
    """Базовая схема бронирования пожелания."""
    comment: Optional[str] = Field(
        None,
        min_length=COMMENT_MIN_LEN,
    )

    class Config:
        extra = Extra.forbid


class ReservationUpdate(ReservationBase):
    """Схема для обновления бронирования пожелания."""
    pass


class ReservationCreate(ReservationUpdate):
    """Схема для создания бронирования пожелания."""
    wish_id: int


class ReservationDB(ReservationBase):
    """Схема бронирования пожелания в БД."""
    id: int
    wish_id: int
    create_date: datetime = Field(
        ...,
        example=CREATE_DATE,
    )
    close_date: Optional[datetime]
    user_id: int

    class Config:
        orm_mode = True
