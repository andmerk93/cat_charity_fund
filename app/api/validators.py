from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject
from app.schemas.charityproject import CharityProjectUpdate


async def check_charity_project_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    """Корутина проверяет существует ли проект с таким именем."""
    charity_project_id = await charity_project_crud.get_project_id_by_name(
        charity_project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )
