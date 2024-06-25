from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_charity_project_not_exists,
    check_full_amount_not_less_than_invested,
    check_not_fully_invested,
    check_no_invested_funds,
)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectRead,
    CharityProjectUpdate
)
from app.core.user import current_superuser
from app.services.investing import invest

router = APIRouter()


@router.post('/', response_model=CharityProjectRead)
async def create_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
        _=Depends(current_superuser)
):
    await check_charity_project_exists(charityproject.name, session)
    new_project = await charity_project_crud.create(charityproject, session)
    new_project = await invest(session, new_project)
    return new_project


@router.get('/', response_model=list[CharityProjectRead])
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.patch('/{project_id}', response_model=CharityProjectRead)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
        _=Depends(current_superuser)
):
    charity_project = await charity_project_crud.get(project_id, session)
    await check_charity_project_not_exists(charity_project)
    await check_full_amount_not_less_than_invested(
        obj_in.full_amount, charity_project)
    await check_not_fully_invested(charity_project)
    if obj_in.name:
        await check_charity_project_exists(obj_in.name, session)
    updated_project = await charity_project_crud.update(
        charity_project, obj_in, session)
    return updated_project


@router.delete('/{project_id}', response_model=CharityProjectRead)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
        _=Depends(current_superuser)
):
    charity_project = await charity_project_crud.get(project_id, session)
    await check_charity_project_not_exists(charity_project)
    await check_no_invested_funds(charity_project)
    await charity_project_crud.remove(charity_project, session)
    return charity_project
