from fastapi import APIRouter

from app.api.endpoints import (
    google_api_router,
    charity_project_router,
    donation_router,
    user_router
)

router = APIRouter()

router.include_router(google_api_router, prefix='/google', tags=['Google'])
router.include_router(charity_project_router, prefix='/charity_project',
                      tags=['charity_projects'])
router.include_router(donation_router, prefix='/donation', tags=['donations'])
router.include_router(user_router, tags=['users'])
