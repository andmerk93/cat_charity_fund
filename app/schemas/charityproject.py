from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProject(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        orm_mode = True


class CharityProjectCreate(CharityProject):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProject):

    @validator('name', 'description', 'full_amount')
    def field_not_empty(cls, value: Union[str, int]):
        if not value:
            raise ValueError('Поле не может быть пустым')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
