from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.crud.charityproject import charity_project_crud
from app.models import User
from app.schemas.donation import (
    DonationAdminDB, DonationCreate, DonationDB
)
from app.services.invest import investment

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
    new_donation = donation_crud.create_not_commit(donation, user)
    session.add(new_donation)
    fill_models = await charity_project_crud.get_not_full_invested_objects(session) # noqa
    invested_list = investment(new_donation, fill_models)
    await donation_crud.commit_models(invested_list, session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
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
