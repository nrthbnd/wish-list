from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_wish_not_completed_or_reserved,
                                check_obj_exists)
from app.core.db import get_async_session
from app.crud.wish import wish_crud
from app.crud.reservation import reservation_crud
from app.services.reserving_process import change_wish_status
from app.schemas.reservation import (ReservationCreate, ReservationDB,
                                     ReservationUpdate)
from constants import (CLEAR_ROUTE, RESERVATION_NOT_EXISTS_EXCEPTION,
                       WISH_NOT_EXISTS_EXCEPTION, RESERVATION_ID_ROUTE,
                       SWITCH_FIELD_RESERVED)

router = APIRouter()


@router.post(CLEAR_ROUTE, response_model=ReservationDB)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    """Бронировать пожелание."""
    wish_id = reservation.wish_id

    wish = await check_obj_exists(
        obj_id=wish_id,
        model_crud=wish_crud,
        exception=WISH_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    await check_wish_not_completed_or_reserved(
        wish_id, session=session,
    )
    await change_wish_status(
        wish=wish,
        field_to_switch=SWITCH_FIELD_RESERVED,
        new_reservation_flag=True,
        session=session,
    )
    return await reservation_crud.create(reservation, session)


@router.get(
    CLEAR_ROUTE,
    response_model=list[ReservationDB],
    response_model_exclude_none=True,
)
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session),
) -> list[ReservationDB]:
    """Получить список всех бронирований."""
    return await reservation_crud.get_multi(session)


@router.patch(
    RESERVATION_ID_ROUTE,
    response_model=ReservationDB,
    # dependencies=[Depends(current_superuser)], или хозяин
)
async def partially_update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    """Редактировать существующее бронирование."""
    reservation = await check_obj_exists(
        obj_id=reservation_id,
        model_crud=reservation_crud,
        exception=RESERVATION_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    return await reservation_crud.update(
        reservation, obj_in, session,
    )


@router.delete(
    RESERVATION_ID_ROUTE,
    response_model=ReservationDB,
    # dependencies=[Depends(current_superuser)],
)
async def remove_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить бронирование (Только для суперюзеров и хозяина)."""
    reservation = await check_obj_exists(
        obj_id=reservation_id,
        model_crud=reservation_crud,
        exception=RESERVATION_NOT_EXISTS_EXCEPTION,
        session=session,
    )
    wish = await wish_crud.get(reservation.wish_id, session)
    await change_wish_status(
        wish=wish,
        field_to_switch=SWITCH_FIELD_RESERVED,
        new_reservation_flag=True,
        session=session,
    )
    return await reservation_crud.remove(reservation, session)
