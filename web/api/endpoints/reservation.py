from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from copy import deepcopy

from api.validators import (check_wish_not_completed_or_reserved,
                            check_author_before_edit, check_obj_exists)
from core.user import current_user, current_superuser
from core.db import get_async_session
from crud.wish import wish_crud
from crud.reservation import reservation_crud
from services.reserving_process import change_wish_status
from schemas.reservation import (ReservationCreate, ReservationDB,
                                 ReservationUpdate)
from models import User
from constants import (CLEAR_ROUTE, RESERVATION_ID_ROUTE,
                       SWITCH_FIELD_RESERVED, WISH_NOT_EXISTS_EXCEPTION,
                       RESERVATION_NOT_EXISTS_EXCEPTION, NOT_ALLOWED_TO_RESERVATION)

router = APIRouter()


@router.post(CLEAR_ROUTE, response_model=ReservationDB)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Бронировать пожелание."""
    wish_id = reservation.wish_id
    user_obj = deepcopy(user)
    wish = await check_obj_exists(
        obj_id=wish_id,
        model_crud=wish_crud,
        exception=WISH_NOT_EXISTS_EXCEPTION,
        session=session)
    await check_wish_not_completed_or_reserved(
        wish_id=wish_id, session=session,
    )
    await change_wish_status(
        wish=wish,
        field_to_switch=SWITCH_FIELD_RESERVED,
        new_reservation_flag=True,
        session=session,
    )
    return await reservation_crud.create(
        obj_in=reservation, session=session, user=user_obj)


@router.get(
    CLEAR_ROUTE,
    response_model=list[ReservationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session),
) -> list[ReservationDB]:
    """Получить список всех бронирований. Только для суперпользователя."""
    return await reservation_crud.get_multi(session=session)


@router.patch(
    RESERVATION_ID_ROUTE,
    response_model=ReservationDB,
)
async def partially_update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Редактировать существующее бронирование."""
    reservation = await check_obj_exists(
        obj_id=reservation_id,
        model_crud=reservation_crud,
        exception=RESERVATION_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    reservation = await check_author_before_edit(
        obj=reservation, user=user, exception=NOT_ALLOWED_TO_RESERVATION,
    )
    return await reservation_crud.update(
        db_obj=reservation, obj_in=obj_in, session=session,
    )


@router.delete(
    RESERVATION_ID_ROUTE,
    response_model=ReservationDB,
)
async def remove_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Удалить бронирование. Только для владельца бронирования или суперпользователя."""
    reservation = await check_obj_exists(
        obj_id=reservation_id,
        model_crud=reservation_crud,
        exception=RESERVATION_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    reservation = await check_author_before_edit(
        obj=reservation, user=user, exception=NOT_ALLOWED_TO_RESERVATION,
    )
    wish = await wish_crud.get(obj_id=reservation.wish_id, session=session)
    await change_wish_status(
        wish=wish,
        field_to_switch=SWITCH_FIELD_RESERVED,
        new_reservation_flag=True,
        session=session,
    )
    return await reservation_crud.remove(db_obj=reservation, session=session)


@router.get(
    '/my_reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'},
)
async def get_my_reservations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех бронирований для текущего пользователя."""
    reservations = await reservation_crud.get_reservation_by_user(
        session=session, user=user,
    )
    return reservations
