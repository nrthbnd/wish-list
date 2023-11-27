from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from constants import (WISH_NAME_MIN_LEN, WISH_NAME_MAX_LEN,
                       CREATE_DATE, EMPTY_FIELD_ERROR)


class WishBase(BaseModel):
    """Базовая схема пожелания."""
    name: Optional[str] = Field(
        None,
        min_length=WISH_NAME_MIN_LEN,
        max_length=WISH_NAME_MAX_LEN,
    )
    comment: Optional[str] = Field(
        None,
    )

    class Config:
        extra = Extra.forbid


class WishCreate(WishBase):
    """Схема для создания пожелания."""
    name: str = Field(
        ...,
        min_length=WISH_NAME_MIN_LEN,
        max_length=WISH_NAME_MAX_LEN,
    )


class WishUpdate(WishBase):
    """Схема для обновления полей пожелания."""

    @validator('name')
    def field_cannot_be_null(cls, value, field):
        if value is None:
            raise ValueError(EMPTY_FIELD_ERROR.format(field.name))
        return value


class WishDB(WishCreate):
    """Схема пожелания в БД."""
    id: int
    create_date: datetime = Field(
        ...,
        example=CREATE_DATE,
    )
    close_date: Optional[datetime]
    completed: bool
    reserved: bool

    class Config:
        orm_mode = True
