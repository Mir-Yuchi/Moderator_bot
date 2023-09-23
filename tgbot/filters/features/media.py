from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from redis.asyncio import Redis

from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings


class MediaActive(BoundFilter):
    key = 'media_delete_active'

    def __init__(self, media_delete_active: bool):
        self.media_delete_active = media_delete_active

    async def check(self, message: Message) -> bool:
        redis: Redis = message.bot['redis_db']
        settings = await RedisTgBotSettings(
            message.chat.id
        ).load_settings(redis)
        if not settings:
            return False
        media_settings = settings[FeaturesList.filter_media.name]
        if any([
            not media_settings['on'],
            not self.media_delete_active,
        ]):
            return False
        return True
