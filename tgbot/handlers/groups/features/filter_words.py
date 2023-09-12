from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from redis.asyncio import Redis

from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings
from tgbot.utils.decorators import only_chat_users_handler


@only_chat_users_handler
async def delete_filter_words(message: Message):
    redis: Redis = message.bot['redis_db']
    settings = await RedisTgBotSettings(
        message.chat.id
    ).load_settings(redis)
    silence_settings = settings[FeaturesList.silence_mode.name]
    if not silence_settings['on']:
        await message.reply('Запрещённое сообщение удалено')
    await message.delete()
    await message.bot.restrict_chat_member(
        message.chat.id, message.from_user.id, None,
        can_add_web_page_previews=False,
        can_send_other_messages=False,
        can_send_media_messages=False,
        can_send_messages=False
    )


def register_filter_words_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_filter_words, subscribe_active=True,
        filter_words_active=True, filter_word_equal=True,
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    )
