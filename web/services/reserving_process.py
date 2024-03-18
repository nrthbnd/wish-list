from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from models import Wish
from crud.reservation import reservation_crud
from constants import SWITCH_FIELD_COMPLETED


async def change_wish_status(
    wish: Wish,
    field_to_switch: str,
    new_reservation_flag: bool,
    session: AsyncSession,
):
    """Изменить статус пожелания."""
    current_value = getattr(wish, field_to_switch)
    new_value = not current_value
    setattr(wish, field_to_switch, new_value)

    if new_reservation_flag is False:
        reservation = await reservation_crud.get_reservation_by_wish_id(
            wish.id, session,
        )
        if field_to_switch == SWITCH_FIELD_COMPLETED and new_value is True:
            wish.close_date = datetime.now()
            if reservation:
                reservation.close_date = datetime.now()
        else:
            wish.close_date, reservation.close_date = None, None

    session.add(wish)
    await session.commit()
    await session.refresh(wish)
