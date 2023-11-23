from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.wish import Wish


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
        db_wish_id = db_wish_id.scalars().first()
        return db_wish_id

    async def get_wish_by_id(
            self,
            wish_id: int,
            session: AsyncSession,
    ) -> Optional[Wish]:
        """Получить пожелание по id."""
        db_wish = await session.execute(
            select(Wish).where(
                Wish.id == wish_id,
            )
        )
        return db_wish.scalars().first()


wish_crud = CRUDWish(Wish)
