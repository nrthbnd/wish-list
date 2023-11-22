from fastapi import APIRouter

from constants import WISH_ROUTER_PREFIX, WISH_ROUTER_TAG
from app.api.endpoints import (
    wish_router,
)

main_router = APIRouter()

main_router.include_router(
    wish_router,
    prefix=WISH_ROUTER_PREFIX,
    tags=[WISH_ROUTER_TAG],
)
