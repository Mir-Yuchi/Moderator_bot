from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from redis.asyncio import Redis

from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings


class MetaDeleteActive(BoundFilter):
    key = 'meta_delete_active'

    def __init__(self, meta_delete_active: bool):
        self.meta_delete_active = meta_delete_active

    async def check(self, message: Message) -> bool:
        redis: Redis = message.bot['redis_db']
        model = RedisTgBotSettings(message.chat.id)
        settings: dict | None = await model.load_settings(redis)
        meta_settings: dict = settings[FeaturesList.meta_info_delete.name]
        if any([
            not settings,
            not self.meta_delete_active,
            not meta_settings['on']
        ]):
            return False
        return True
