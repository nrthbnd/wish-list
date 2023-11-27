from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_before_delete,
                                check_obj_exists)
from app.core.db import get_async_session
from app.crud.wish import wish_crud
from app.services.reserving_process import change_wish_status
from app.schemas.wish import WishCreate, WishDB, WishUpdate
from constants import (WISH_NOT_EXISTS_EXCEPTION, CLEAR_ROUTE, WISH_ID_ROUTE,
                       SWITCH_FIELD_COMPLETED)


router = APIRouter()


@router.post(
    CLEAR_ROUTE,
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
    WISH_ID_ROUTE,
    response_model=WishDB,
    response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)], или хозяин
)
async def partially_update_wish(
    wish_id: int,
    obj_in: WishUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Редактировать существующее пожелание (Только для суперюзеров)."""
    wish = await check_obj_exists(
        obj_id=wish_id,
        model_crud=wish_crud,
        exception=WISH_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    return await wish_crud.update(wish, obj_in, session)


@router.delete(
    WISH_ID_ROUTE,
    response_model=WishDB,
    # dependencies=[Depends(current_superuser)],
)
async def remove_wish(
    wish_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить пожелание (Только для суперюзеров)."""
    wish = await check_obj_exists(
        obj_id=wish_id,
        model_crud=wish_crud,
        exception=WISH_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    await check_before_delete(wish_id, session)
    return await wish_crud.remove(wish, session)


@router.get(
    CLEAR_ROUTE,
    response_model=list[WishDB],
    response_model_exclude_none=True,
)
async def get_all_wishes(
    session: AsyncSession = Depends(get_async_session),
) -> list[WishDB]:
    """Получить список всех пожеланий."""
    return await wish_crud.get_multi(session)


@router.post(
    WISH_ID_ROUTE,
    response_model=WishDB,
    # dependencies=[Depends(current_user)],
    response_model_exclude_none=True,
)
async def change_wish_completed_status(
    wish_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Изменить статус пожелания - выполнено/не выполнено."""
    # проверить, что это делает только автор
    wish = await check_obj_exists(
        obj_id=wish_id,
        model_crud=wish_crud,
        exception=WISH_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    await change_wish_status(
        wish=wish,
        field_to_switch=SWITCH_FIELD_COMPLETED,
        new_reservation=False,
        session=session,
    )
    return wish
