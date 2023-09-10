from Levenshtein import ratio
from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from redis.asyncio import Redis

from tgbot.config import Config
from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings
from tgbot.utils.text import replace_word_letters


async def delete_obscene(message: Message):
    config: Config = message.bot['config']
    redis: Redis = message.bot['redis_db']
    settings = await RedisTgBotSettings(
        message.chat.id
    ).load_settings(redis)
    silent_mode = settings[FeaturesList.silence_mode.name]
    phrase = replace_word_letters(message.text.lower().replace(' ', ''))
    with open(config.misc.OBSCENE_WORDS_FILE, encoding='utf-8') as file:
        for word in file:
            found_word = False
            for part in range(len(phrase)):
                fragment = phrase[part: part + len(word)]
                distance = ratio(fragment, word)
                if distance >= .7:
                    if not silent_mode['on']:
                        await message.reply('Маты запрещены в чате 👮🏻')
                    found_word = True
                    break
            if found_word:
                await message.delete()
                break


def register_obscene_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_obscene, subscribe_active=True,
        delete_obscene_active=True,
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    )
