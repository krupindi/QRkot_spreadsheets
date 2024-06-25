from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from aiogoogle import Aiogoogle

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.services.google_api import (
    spreadsheets_create,
    set_user_permissions,
    spreadsheets_update_value
)
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectRead)

router = APIRouter()


@router.post('/', response_model=list[CharityProjectRead])
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service),
        _=Depends(current_superuser)
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session)
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid, projects, wrapper_services)
    return projects
