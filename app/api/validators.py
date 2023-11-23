from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from constants import (
    NAME_DUPLICATE_EXCEPTION, WISH_NOT_EXISTS_EXCEPTION,
    WISH_ALREADY_RESERVED, WISH_ALREADY_COMPLETED,
)
from app.crud.wish import wish_crud
from app.models import Wish, Reservation


async def check_name_duplicate(
        wish_name: str,
        session: AsyncSession,
) -> None:
    """Проверить уникальность полученного названия пожелания."""
    wish_id = await wish_crud.get_wish_id_by_name(
        wish_name, session,
    )
    if wish_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NAME_DUPLICATE_EXCEPTION,
        )


async def check_wish_exists(
        wish_id: int,
        session: AsyncSession,
) -> Wish:
    """Проверить, существует ли пожелание по id."""
    wish = await wish_crud.get_wish_by_id(
        wish_id, session,
    )
    if wish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=WISH_NOT_EXISTS_EXCEPTION,
        )
    return wish


async def check_wish_not_completed_or_reserved(
        wish_id: int,
        session: AsyncSession,
):
    """Проверить, не было ли желание выполнено или забронировано."""
    # Проверка в таблице бронирований
    was_reserved = await session.execute(
        select(Reservation).where(
             Reservation.wish_id == wish_id,
        )
    )

    if was_reserved.scalars().first() is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=WISH_ALREADY_RESERVED,
        )

    # Проверка в таблице пожеланий
    fields = await session.execute(
        select(
            Wish.reserved,
            Wish.completed,
        ).where(
            Wish.id == wish_id,
        )
    )
    fields = fields.all()
    fields = dict(fields[0])

    if fields['reserved'] is not False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=WISH_ALREADY_RESERVED,
        )
    if fields['completed'] is not False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=WISH_ALREADY_COMPLETED,
        )
