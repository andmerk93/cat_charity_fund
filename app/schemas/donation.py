from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class Donation(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(Donation):
    pass


class DonationDB(Donation):
    id: int
    create_date: datetime


class DonationAdminDB(DonationDB):
    user_id: str
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
