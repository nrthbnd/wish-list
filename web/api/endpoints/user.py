from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.user import auth_backend, fastapi_users, current_user
from core.db import get_async_session
from crud.wish import wish_crud
from crud.user import user_crud
from schemas.user import UserCreate, UserRead, UserUpdate
from schemas.wish import WishDB

from constants import USER_WISHES, USERS_ROUTER_TAG, USERS_ROUTER_PREFIX

router = APIRouter()

router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=USERS_ROUTER_PREFIX,
    tags=[USERS_ROUTER_TAG],
)


@router.delete(
    '/users/{id}',
    tags=[USERS_ROUTER_TAG],
    deprecated=True
)
def delete_user(id: str):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=405,
        detail="Удаление пользователей запрещено!"
    )


@router.get(
    USER_WISHES,
    tags=[USERS_ROUTER_TAG],
    response_model=list[WishDB],
    response_model_exclude_none=True,
    # dependencies=[Depends(current_user)],  # Вернуть обязательно после настройки авторизации
)
async def get_wishes_by_user_first_name(
    user_first_name: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[WishDB]:
    """Получить список пожеланий конкретного пользователя."""
    user_id = await user_crud.get_user_id_by_first_name(first_name=user_first_name, session=session)
    return await wish_crud.get_wishes_by_user_id(user_id=user_id, session=session)


# @router.get(
#     USER_WISHES,
#     tags=[USERS_ROUTER_TAG],
#     response_model=list[WishDB],
#     response_model_exclude_none=True,
#     # dependencies=[Depends(current_user)],  # Вернуть обязательно после настройки авторизации
# )
# async def get_user_name_by_id(
#     user_id: int,
#     session: AsyncSession = Depends(get_async_session),
# ) -> list[WishDB]:
#     """Получить имя пользователя по его id."""
#     user_info = await user_crud.get(obj_id=user_id, session=session)
#     return user_info.first_name
