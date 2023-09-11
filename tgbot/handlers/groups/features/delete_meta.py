from aiogram import Dispatcher
from aiogram.types import Message, ChatType, ContentType
from redis.asyncio import Redis

from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings


async def delete_meta_info(message: Message):
    if message.content_type == ContentType.NEW_CHAT_MEMBERS:
        redis: Redis = message.bot['redis_db']
        settings = await RedisTgBotSettings(
            message.chat.id
        ).load_settings(redis)
        filter_settings = settings[FeaturesList.filter_words.name]
        silence_settings = settings[FeaturesList.silence_mode.name]
        words = filter_settings['words_list']
        if filter_settings['on'] and words:
            for user in message.new_chat_members:
                for word in words:
                    if word in user.full_name.lower():
                        await message.bot.ban_chat_member(
                            message.chat.id,
                            user.id
                        )
                        if not silence_settings['on']:
                            await message.reply(
                                'Пользователь был забанен из-за запрещенного '
                                'ника'
                            )
                        break
    await message.delete()


def register_meta_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_meta_info, subscribe_active=True,
        meta_delete_active=True,
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
        content_types=[
            ContentType.LEFT_CHAT_MEMBER,
            ContentType.NEW_CHAT_MEMBERS,
            ContentType.NEW_CHAT_PHOTO,
            ContentType.NEW_CHAT_TITLE,
            ContentType.DELETE_CHAT_PHOTO,
        ]
    )
