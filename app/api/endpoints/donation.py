from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationRead,
    DonationDB,
    DonationResponse
)
from app.core.user import current_user, current_superuser
from app.services.investing import invest

router = APIRouter()


@router.post('/', response_model=DonationResponse)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user=Depends(current_user)
):
    donation.user_id = user.id
    new_donation = await donation_crud.create(donation, session)
    new_donation = await invest(session, new_donation)
    await session.refresh(new_donation)
    return new_donation


@router.get('/my', response_model=list[DonationDB])
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user=Depends(current_user)
):
    donations = await donation_crud.get_by_user(user.id, session)
    return donations


@router.get('/', response_model=list[DonationRead])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
        _=Depends(current_superuser)
):
    donations = await donation_crud.get_multi(session)
    return donations
