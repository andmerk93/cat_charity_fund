from http import HTTPStatus

from fastapi import HTTPException

from app.models import CharityProject


def check_charity_project_name_duplicate(
        charity_project_name: str,
        charity_project: CharityProject,
):
    if (
        charity_project is not None and
        charity_project.name == charity_project_name
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


def check_charity_project_exists(charity_project: CharityProject):
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проекта с таким ID нет в базе!',
        )


def check_project_is_investing(charity_project: CharityProject):
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


def check_project_is_fully_invested(charity_project: CharityProject):
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )


def check_full_amount_is_less_than_invested(
    new_full_amount: int,
    invested_amount: int
):
    if (
        new_full_amount is not None and
        new_full_amount < invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Сумма не может быть меньше внесённой!',
        )
