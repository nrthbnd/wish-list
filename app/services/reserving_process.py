from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Wish


async def change_wish_status(
    wish: Wish,
    field_to_switch: str,
    session: AsyncSession,
):
    """Изменить статус пожелания."""
    current_value = getattr(wish, field_to_switch)
    new_value = not current_value
    setattr(wish, field_to_switch, new_value)

    session.add(wish)
    await session.commit()
    await session.refresh(wish)
