from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class Donation(BaseModel):
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        orm_mode = True


class DonationCreate(Donation):
    comment: Optional[str]


class DonationDB(DonationCreate):
    id: int
    create_date: datetime


class DonationAdminDB(DonationDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
