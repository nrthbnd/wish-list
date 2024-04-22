from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models import Wish


class CRUDWish(CRUDBase):
    """CRUD-операции с пожеланиями."""

    async def get_wish_id_by_name(
        self,
        wish_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получить id пожелания по его названию."""
        db_wish_id = await session.execute(
            select(Wish.id).where(
                Wish.name == wish_name
            )
        )
        return db_wish_id.scalars().first()

    async def get_wishes_by_user_id(
        self,
        user_id: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получить пожелания по id его создателя."""
        db_wishes = await session.execute(
            select(Wish).where(
                Wish.user_id == user_id
            )
        )
        return db_wishes.scalars().all()


wish_crud = CRUDWish(Wish)
