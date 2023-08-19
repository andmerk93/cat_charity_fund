from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.models import Donation
from app.schemas.charityproject import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.api.validators import (
    check_charity_project_name_duplicate,
    check_charity_project_exists,
    check_project_is_investing,
    check_full_amount_is_less_than_invested,
    check_project_is_fully_invested
)
from app.services.invest import investing_process

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Создает благотворительный проект.
    """
    project = await charity_project_crud.get_project_by_name(
        charity_project.name, session
    )
    check_charity_project_name_duplicate(charity_project.name, project)
    new_project = await charity_project_crud.create(charity_project, session)
    await investing_process(new_project, Donation, session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    charity_project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """
    project_by_id = await charity_project_crud.get(project_id, session)
    check_charity_project_exists(project_by_id)
    check_project_is_fully_invested(project_by_id)
    check_full_amount_is_less_than_invested(
        charity_project.full_amount, project_by_id.invested_amount
    )
    check_charity_project_name_duplicate(charity_project.name, project_by_id)
    project_by_name = await charity_project_crud.get_project_by_name(
        charity_project.name, session
    )
    check_charity_project_name_duplicate(charity_project.name, project_by_name)
    project = await charity_project_crud.update(
        project_by_id, charity_project, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Удаляет проект.
    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """
    project = await charity_project_crud.get(project_id, session)
    check_project_is_investing(project)
    project = await charity_project_crud.remove(project, session)
    return project
