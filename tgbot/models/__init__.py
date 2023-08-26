from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base
import sqlalchemy as sa

BASE = declarative_base()


class AsyncBaseModelMixin:

    @classmethod
    async def all(cls, session: AsyncSession) -> Sequence:
        query = sa.select(cls)
        result = await session.execute(query)
        return result.scalars().all()
