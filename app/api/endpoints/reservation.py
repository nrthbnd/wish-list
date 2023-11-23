from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_wish_exists, check_wish_not_completed_or_reserved,
)
from app.core.db import get_async_session
from app.crud.wish import wish_crud
from app.crud.reservation import reservation_crud
from app.services.reserving_process import change_wish_status
from app.schemas.reservation import (
    ReservationCreate, ReservationDB,
)

router = APIRouter()


@router.post('/', response_model=ReservationDB)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    """Бронировать пожелание."""
    await check_wish_exists(
        reservation.wish_id, session,
    )
    await check_wish_not_completed_or_reserved(
        reservation.wish_id, session=session,
    )
    wish = await wish_crud.get_wish_by_id(reservation.wish_id, session)
    await change_wish_status(
        wish=wish,
        field_to_switch='reserved',
        session=session,
    )
    return await reservation_crud.create(
        reservation, session,
    )
