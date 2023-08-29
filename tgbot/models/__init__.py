from typing import Union, Any

from sqlalchemy import MetaData, JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as sa


class BASE(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_name)s',
            'ck': 'ck_%(table_name)s_`%(constraint_name)s`',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%'
                  '(referred_table_name)s',
            'pk': 'pk_%(table_name)s',
        }
    )
    type_annotation_map = {dict[Union[str, int], Any]: JSON}


class AsyncBaseModelMixin:

    @classmethod
    def filter(cls, stmt: Union[sa.Select, sa.Update, sa.Delete],
               filter_data: dict):
        for key, value in filter_data.items():
            split_field = key.split('__')
            if len(split_field) < 2:
                stmt.where(getattr(cls, key) == value)
        return stmt

    @classmethod
    async def get_all(cls, session: AsyncSession,
                      filter_data: dict | None = None) -> list:
        query = sa.select(cls)
        if filter_data:
            query = cls.filter(query, filter_data)
        result = await session.execute(query)
        return result.scalars().all()  # type: ignore

    @classmethod
    async def create(cls, session: AsyncSession, data: dict) -> object:
        obj = cls(**data)
        session.add(obj)
        await session.commit()
        return obj

    @classmethod
    async def update(cls, session: AsyncSession,
                     filter_data: dict, update_data: dict):
        stmt = (
            sa.update(cls)
            .values(**update_data)
            .returning(cls)
        )
        if filter_data:
            stmt = cls.filter(stmt, filter_data)
        result = await session.execute(stmt)
        obj: cls | None = result.scalars().first()
        await session.commit()
        return obj

    @classmethod
    async def bulk_create(cls, session: AsyncSession,
                          data_list: list[dict]) -> list:
        obj_list = []
        for data in data_list:
            obj = cls(**data)
            obj_list.append(obj)
        session.add_all(obj_list)
        await session.commit()
        return obj_list
