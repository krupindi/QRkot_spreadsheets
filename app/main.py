from fastapi import FastAPI

from app.api.routers import router
from app.core.config import settings
from app.core.init_db import create_first_superuser

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)

app.include_router(router)


@app.on_event("startup")
async def startup():
    await create_first_superuser()
