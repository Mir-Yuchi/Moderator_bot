from aiogram import Dispatcher
from aiogram.types import Message, ChatType, ChatPermissions
from redis.asyncio import Redis

from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings


async def delete_filter_words(message: Message):
    chat_admins = await message.chat.get_administrators()
    for admin in chat_admins:
        if admin.user.id == message.from_user.id:
            return
    redis: Redis = message.bot['redis_db']
    settings = await RedisTgBotSettings(
        message.chat.id
    ).load_settings(redis)
    silence_settings = settings[FeaturesList.silence_mode.name]
    if not silence_settings['on']:
        await message.reply('Запрещённое сообщение удалено')
    await message.delete()
    await message.bot.restrict_chat_member(
        message.chat.id,
        message.from_user.id,
        ChatPermissions(False, False, False, False, False, False,
                        False, False, False, False, False, False,
                        False, False, False)
    )


def register_filter_words_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_filter_words, subscribe_active=True,
        filter_words_active=True, filter_word_equal=True,
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    )
