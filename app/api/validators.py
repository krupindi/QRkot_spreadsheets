from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.crud.charity_project import charity_project_crud
from app.core.config import settings


async def check_charity_project_exists(name: str, session: AsyncSession):
    project = await charity_project_crud.get_by_name(name, session)
    if project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Благотворительный проект с таким именем уже существует'
        )


async def check_charity_project_not_exists(project):
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Благотворительный проект не найден'
        )


async def check_full_amount_not_less_than_invested(full_amount,
                                                   charity_project):
    if (full_amount is not None and
            full_amount < charity_project.invested_amount):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Общая сумма не может быть меньше инвестированной суммы'
        )


async def check_not_fully_invested(charity_project):
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя обновить полностью инвестированный проект'
        )


async def check_no_invested_funds(charity_project):
    if charity_project.invested_amount > settings.MIN_INVESTED_AMOUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалить проект с уже инвестированными средствами'
        )
