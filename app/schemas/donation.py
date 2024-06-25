from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, validator


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None

    @validator('full_amount')
    def amount_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Полная сумма должна быть больше нуля')
        return value


class DonationCreate(DonationBase):
    user_id: Optional[int] = None


class DonationUpdate(DonationBase):
    pass


class DonationRead(DonationBase):
    id: int
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    user_id: int

    class Config:
        orm_mode = True


class DonationResponse(BaseModel):
    id: int
    full_amount: PositiveInt
    create_date: datetime
    comment: Optional[str] = None

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
