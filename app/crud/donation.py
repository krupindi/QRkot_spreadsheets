from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    async def get_by_user(
            self,
            user_id: int,
            db: AsyncSession
    ) -> List[Donation]:
        result = await db.execute(
            select(self.model).filter(self.model.user_id == user_id))
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
