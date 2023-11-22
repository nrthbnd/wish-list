from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from constants import (
    NAME_DUPLICATE_EXCEPTION, WISH_NOT_EXISTS_EXCEPTION,
)
from app.crud.wish import wish_crud
from app.models import Wish


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
