from fastapi import APIRouter

from constants import (
    WISH_ROUTER_PREFIX, WISH_ROUTER_TAG,
    RES_ROUTER_PREFIX, RES_ROUTER_TAG,
)
from api.endpoints import (
    wish_router, reservation_router,
)

main_router = APIRouter()

main_router.include_router(
    wish_router,
    prefix=WISH_ROUTER_PREFIX,
    tags=[WISH_ROUTER_TAG],
)
main_router.include_router(
    reservation_router,
    prefix=RES_ROUTER_PREFIX,
    tags=[RES_ROUTER_TAG],
)
