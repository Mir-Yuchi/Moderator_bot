import json
from dataclasses import dataclass
from typing import Any, Union

import sqlalchemy as sa
from redis.asyncio import Redis
from sqlalchemy.orm import mapped_column, Mapped

from . import BASE, AsyncBaseModelMixin
from .client import BotClient


class UserTgGroupBot(BASE, AsyncBaseModelMixin):
    __tablename__ = 'user_tg_group_bots'

    group_id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.BIGINT, sa.ForeignKey(
        f'{BotClient.__tablename__}.tg_id'
    ))
    bot_settings: Mapped[dict[Union[str, int], Any]]


@dataclass
class RedisTgBotSettings:
    owner_tg_id: int
    group_id: str
    settings: dict[Union[str, int], Any]

    @property
    def db_settings_key(self) -> str:
        return f'group_bot_settings_{self.owner_tg_id}:{self.group_id}'

    @property
    def raw_settings(self) -> str:
        return json.dumps(self.settings)

    async def set_settings(self, redis: Redis):
        result = await redis.set(
            self.db_settings_key,
            self.raw_settings
        )
        return result
