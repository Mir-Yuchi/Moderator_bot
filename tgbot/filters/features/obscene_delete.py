from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from redis.asyncio import Redis

from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings


class ObsceneDeleteActive(BoundFilter):
    key = 'delete_obscene_active'

    def __init__(self, delete_obscene_active: bool):
        self.delete_obscene_active = delete_obscene_active

    async def check(self, message: Message) -> bool:
        redis: Redis = message.bot['redis_db']
        model = RedisTgBotSettings(message.chat.id)
        settings: dict | None = await model.load_settings(redis)
        obscene_settings: dict = settings[FeaturesList.obscene_delete.name]
        if any([
            not settings,
            not self.delete_obscene_active,
            not obscene_settings['on']
        ]):
            return False
        return True
