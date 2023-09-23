from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from redis.asyncio import Redis

from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings


class IsSubscribeActiveFilter(BoundFilter):
    key = 'subscribe_active'

    def __init__(self, subscribe_active: bool):
        self.subscribe_active = subscribe_active

    async def check(self, message: Message) -> bool:
        redis: Redis = message.bot['redis_db']
        model = RedisTgBotSettings(message.chat.id)
        settings: dict | None = await model.load_settings(redis)
        if not settings or not self.subscribe_active:
            return False
        return True
