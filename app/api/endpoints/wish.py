from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_wish_exists
from app.core.db import get_async_session
from app.crud.wish import wish_crud
from app.schemas.wish import (
    WishCreate, WishDB, WishUpdate,
)


router = APIRouter()


@router.post(
    '/',
    response_model=WishDB,
    # dependencies=[Depends(current_user)],
    response_model_exclude_none=True,
)
async def create_new_wish(
    wish: WishCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создать новое пожелание."""
    await check_name_duplicate(wish.name, session)
    return await wish_crud.create(wish, session)


@router.patch(
    '/{wish_id}',
    response_model=WishDB,
    # dependencies=[Depends(current_superuser)], или хозяин
)
async def partially_update_wish(
    wish_id: int,
    obj_in: WishUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Редактировать существующее пожелание (Только для суперюзеров)."""
    wish = await check_wish_exists(
        wish_id, session,
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    return await wish_crud.update(
        wish, obj_in, session,
    )


@router.delete(
    '/{wish_id}',
    response_model=WishDB,
    # dependencies=[Depends(current_superuser)],
)
async def remove_wish(
    wish_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить пожелание (Только для суперюзеров)."""
    wish = await check_wish_exists(
        wish_id, session,
    )

    return await wish_crud.remove(
        wish, session,
    )


@router.get(
    '/',
    response_model=list[WishDB],
    response_model_exclude_none=True,
)
async def get_all_wishes(
    session: AsyncSession = Depends(get_async_session),
) -> list[WishDB]:
    """Получить список всех пожеланий."""
    return await wish_crud.get_multi(session)
