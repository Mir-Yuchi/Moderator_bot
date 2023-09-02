import json
from dataclasses import dataclass
from typing import Any, Union

from redis.asyncio import Redis


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
