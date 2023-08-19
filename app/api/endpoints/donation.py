from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationAdminDB, DonationCreate, DonationDB
)

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationAdminDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Получает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    dependencies=[Depends(current_user)],
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Сделать пожертвование.
    """
    new_donation = await donation_crud.create(donation, session, user)
    return new_donation


@router.get(
    '/me',
    response_model=List[DonationDB],
    dependencies=[Depends(current_user)],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Получить список моих пожертвований.
    """
    return await donation_crud.get_by_user(session, user)
