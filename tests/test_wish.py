import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.wish import CRUDWish
from app.models.wish import Wish


# @pytest.mark.asyncio
# async def test_get_wish_id_by_name():
    # Создание инмемори базы данных для тестов
    # Инициализация CRUDWish с фейковыми данными
    # Вызов метода get_wish_id_by_name с заданным названием пожелания
    # Проверка результата

    # Пример теста:
    # async with AsyncSession() as session:
    #     wish_crud = CRUDWish(Wish)
    #     result = await wish_crud.get_wish_id_by_name("Test Wish", session)
    #     assert result is not None


@pytest.mark.asyncio
async def test_get_wish_id_by_name(db_session: AsyncSession):
    # Создаем экземпляр CRUDWish
    crud_wish = CRUDWish(Wish)

    # Создаем тестовые данные
    test_wish = Wish(name="test_wish")
    db_session.add(test_wish)
    await db_session.commit()
    await db_session.refresh(test_wish)

    # Получаем id пожелания по его названию
    wish_id = await crud_wish.get_wish_id_by_name("test_wish", db_session)

    # Проверяем, что id соответствует id созданного пожелания
    assert wish_id == test_wish.id

    # Проверяем, что метод возвращает None, если пожелания не существует
    wish_id = await crud_wish.get_wish_id_by_name("non_existent_wish", db_session)
    assert wish_id is None
