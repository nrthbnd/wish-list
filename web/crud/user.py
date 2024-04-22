from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models import User


class CRUDUser(CRUDBase):
    """CRUD-операции с пользователями."""

    async def get_user_id_by_first_name(
        self,
        first_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получить id пользователя по его first_name."""
        db_user_id = await session.execute(
            select(User.id).where(
                User.first_name == first_name
            )
        )
        return db_user_id.scalars().first()


user_crud = CRUDUser(User)
