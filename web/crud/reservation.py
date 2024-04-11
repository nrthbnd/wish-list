from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models import Reservation, User


class CRUDReservation(CRUDBase):
    """CRUD-операции с бронированиями."""

    async def get_reservation_by_wish_id(
        self,
        wish_id: int,
        session: AsyncSession,
    ) -> Optional[Reservation]:
        """Получить бронирование по id пожелания."""
        db_reservation = await session.execute(
            select(Reservation).where(
                Reservation.wish_id == wish_id
            )
        )
        return db_reservation.scalars().first()

    async def get_reservation_by_user(
        self,
        session: AsyncSession,
        user: User,
    ):
        """Получить бронирования определенного пользователя."""
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.user_id == user.id
            )
        )
        return reservations.scalars().all()


reservation_crud = CRUDReservation(Reservation)
