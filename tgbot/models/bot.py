import json
from dataclasses import dataclass
from typing import Any, Union

from redis.asyncio import Redis


@dataclass
class RedisTgBotSettings:
    group_id: str | int
    settings: dict[Union[str, int], Any] | None = None

    async def load_settings(self, redis: Redis) -> dict | None:
        raw_settings = await redis.get(self.db_settings_key)
        if not raw_settings:
            return
        return json.loads(raw_settings)

    @property
    def db_settings_key(self) -> str:
        return f'group_bot_settings_{self.group_id}'

    @property
    def raw_settings(self) -> str:
        return json.dumps(self.settings)

    async def set_settings(self, redis: Redis):
        result = await redis.set(
            self.db_settings_key,
            self.raw_settings
        )
        return result
