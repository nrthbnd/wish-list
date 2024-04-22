from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routers import main_router
from core.config import settings
from core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(main_router)


origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
