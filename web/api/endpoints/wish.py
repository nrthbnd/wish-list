from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.validators import (check_name_duplicate, check_before_delete,
                            check_author_before_edit, check_obj_exists)
from core.user import current_user, current_superuser
from core.db import get_async_session
from crud.wish import wish_crud
from services.reserving_process import change_wish_status
from schemas.wish import WishCreate, WishDB, WishUpdate
from models import User
from constants import (WISH_NOT_EXISTS_EXCEPTION, CLEAR_ROUTE, WISH_ID_ROUTE,
                       SWITCH_FIELD_COMPLETED, NOT_ALLOWED_TO_WISH)


router = APIRouter()


@router.post(
    CLEAR_ROUTE,
    response_model=WishDB,
    response_model_exclude_none=True,
    response_model_exclude={'create_date'},
)
async def create_new_wish(
    wish: WishCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создать новое пожелание."""
    await check_name_duplicate(wish_name=wish.name, session=session)
    return await wish_crud.create(obj_in=wish, session=session, user=user)


@router.patch(
    WISH_ID_ROUTE,
    response_model=WishDB,
    response_model_exclude_none=True,
    response_model_exclude={'create_date'},
)
async def partially_update_wish(
    wish_id: int,
    obj_in: WishUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Редактировать существующее пожелание.
    Только для владельца пожелания или суперпользователя."""
    wish = await check_obj_exists(
        obj_id=wish_id,
        model_crud=wish_crud,
        exception=WISH_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    wish = await check_author_before_edit(
        obj=wish, user=user, exception=NOT_ALLOWED_TO_WISH,
    )
    if obj_in.name is not None:
        await check_name_duplicate(wish_name=obj_in.name, session=session)
    return await wish_crud.update(db_obj=wish, obj_in=obj_in, session=session)


@router.delete(
    WISH_ID_ROUTE,
    response_model=WishDB,
)
async def remove_wish(
    wish_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Удалить пожелание. Только для владельца пожелания или суперпользователя."""
    wish = await check_obj_exists(
        obj_id=wish_id,
        model_crud=wish_crud,
        exception=WISH_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    wish = await check_author_before_edit(
        obj=wish, user=user, exception=NOT_ALLOWED_TO_WISH,
    )
    await check_before_delete(wish_id=wish_id, session=session)
    return await wish_crud.remove(db_obj=wish, session=session)


@router.get(
    CLEAR_ROUTE,
    response_model=list[WishDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_wishes(
    session: AsyncSession = Depends(get_async_session),
) -> list[WishDB]:
    """Получить список всех пожеланий. Только для суперпользователя."""
    return await wish_crud.get_multi(session=session)


@router.post(
    WISH_ID_ROUTE,
    response_model=WishDB,
    response_model_exclude_none=True,
)
async def change_wish_completed_status(
    wish_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Изменить статус пожелания - выполнено/не выполнено.
    Только для владельца пожелания или суперпользователя."""
    wish = await check_obj_exists(
        obj_id=wish_id,
        model_crud=wish_crud,
        exception=WISH_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    wish = await check_author_before_edit(
        obj=wish, user=user, exception=NOT_ALLOWED_TO_WISH,
    )
    await change_wish_status(
        wish=wish,
        field_to_switch=SWITCH_FIELD_COMPLETED,
        new_reservation_flag=False,
        session=session,
    )
    return wish
