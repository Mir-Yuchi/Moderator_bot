from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from redis.asyncio import Redis

from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings
from tgbot.utils.text import replace_word_letters


class FilterWordsActive(BoundFilter):
    key = 'filter_words_active'

    def __init__(self, filter_words_active: bool):
        self.filter_words_active = filter_words_active

    async def check(self, message: Message) -> bool:
        redis: Redis = message.bot['redis_db']
        settings = await RedisTgBotSettings(
            message.chat.id
        ).load_settings(redis)
        filter_settings = settings[FeaturesList.filter_words.name]
        if any([
            not settings,
            not self.filter_words_active,
            not filter_settings['on']
        ]):
            return False
        return True


class FilterWordEqual(BoundFilter):
    key = 'filter_word_equal'

    def __init__(self, filter_word_equal: bool):
        self.filter_word_equal = filter_word_equal

    async def check(self, message: Message) -> bool:
        redis: Redis = message.bot['redis_db']
        settings = await RedisTgBotSettings(
            message.chat.id
        ).load_settings(redis)
        filter_settings = settings[FeaturesList.filter_words.name]
        words = filter_settings['words_list']
        phrase = replace_word_letters(message.text.lower())
        if any([
            not settings,
            not self.filter_word_equal,
            phrase not in words,
        ]):
            return False
        return True
