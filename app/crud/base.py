from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    def create_not_commit(
            self,
            obj_in,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        # Если пользователь был передан...
        if user is not None:
            # ...то дополнить словарь для создания модели.
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        return db_obj

    async def commit_models(
            self,
            obj_list,
            session: AsyncSession,
    ):
        session.add_all(obj_list)
        await session.commit()

    async def update(
            self,
            db_obj,  # Объект из БД для обновления
            obj_in,  # Объект из запроса
            session: AsyncSession,
    ):
        # Представляем объект из БД в виде словаря
        obj_data = jsonable_encoder(db_obj)
        # Конвертируем объект с данными из запроса в словарь,
        # исключаем неустановленные пользователем поля
        update_data = obj_in.dict(exclude_unset=True)

        # Перебираем все ключи словаря, сформированного из БД-объекта
        for field in obj_data:
            # Если конкретное поле есть в словаре с данными из запроса, то...
            if field in update_data:
                # ...устанавливаем объекту БД новое значение атрибута
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)            # Добавляем обновленный объект в сессию
        await session.commit()         # Фиксируем изменения
        await session.refresh(db_obj)  # Обновляем объект из БД
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)  # Удаляем объект из БД
        await session.commit()        # Фиксируем изменения в БД
        # Не обновляем объект через метод refresh(), значит,
        # он ещё содержит информацию об удаляемом объекте
        return db_obj

    async def get_not_full_invested_objects(
        self,
        session: AsyncSession
    ):
        objects = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 0
            ).order_by(self.model.create_date)
        )
        return objects.scalars().all()
