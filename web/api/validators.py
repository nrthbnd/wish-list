from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from constants import (NAME_DUPLICATE_EXCEPTION,
                       WISH_ALREADY_RESERVED, WISH_ALREADY_COMPLETED,
                       NOT_ALLOWED_TO_DELETE_WISH, SWITCH_FIELD_COMPLETED,
                       SWITCH_FIELD_RESERVED)
from crud.wish import wish_crud
from models import Wish, Reservation, User


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


async def check_before_delete(
        wish_id: int,
        session: AsyncSession,
):
    """Проверить, можено ли удалять пожелание."""
    wish = await wish_crud.get(wish_id, session)
    if wish.reserved and not wish.completed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=NOT_ALLOWED_TO_DELETE_WISH,
        )


async def check_obj_exists(
        obj_id: int,
        model_crud,
        exception: str,
        session: AsyncSession,
):
    """Проверить, существует ли объект по id."""
    obj = await model_crud.get(
        obj_id=obj_id,
        session=session,
    )
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exception,
        )
    return obj


async def check_wish_not_completed_or_reserved(
        wish_id: int,
        session: AsyncSession,
):
    """Проверить, не было ли желание выполнено или забронировано."""
    # Проверка в таблице бронирований
    was_reserved = await session.execute(
        select(Reservation).where(
             Reservation.wish_id == wish_id))

    if was_reserved.scalars().first() is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=WISH_ALREADY_RESERVED,
        )

    # Проверка в таблице пожеланий
    fields = await session.execute(
        select(Wish.reserved, Wish.completed,
               ).where(Wish.id == wish_id)
    )
    fields = fields.all()
    fields = dict(fields[0])

    if fields[SWITCH_FIELD_RESERVED] is not False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=WISH_ALREADY_RESERVED,
        )
    if fields[SWITCH_FIELD_COMPLETED] is not False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=WISH_ALREADY_COMPLETED,
        )


async def check_author_before_edit(
    obj,
    user: User,
    exception: str,
):
    """Проверить, выполняется ли действие автором объекта."""
    if obj.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail=exception,
        )
    return obj
