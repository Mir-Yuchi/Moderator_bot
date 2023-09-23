from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from redis.asyncio import Redis

from tgbot.data.bot_features import FeaturesList
from tgbot.keyboards.inline import make_user_actions_log
from tgbot.models.bot import RedisTgBotSettings
from tgbot.utils.decorators import only_chat_users_handler
from tgbot.utils.text import mention_user_html


@only_chat_users_handler
async def delete_filter_words(message: Message):
    redis: Redis = message.bot['redis_db']
    settings = await RedisTgBotSettings(
        message.chat.id
    ).load_settings(redis)
    text = message.text
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
    log_chat_settings = settings[FeaturesList.log_chat.name]
    chat_log_id = log_chat_settings['group_id']
    if log_chat_settings['on'] and chat_log_id:
        chat_info = await message.bot.get_chat(message.chat.id)
        mention_user = mention_user_html(
            message.from_user.id, message.from_user.full_name
        )
        await message.bot.send_message(
            chat_log_id,
            f'<b>РЕПОРТ ПОЛЬЗОВАТЕЛЯ ЗА ИСПОЛЬЗОВАНИЕ ЗАПРЕЩЁННОЕ СЛОВО</b>\n'
            f'<b>ЧАТ</b>\n🆔: {chat_info.id}\n'
            f'Название: {chat_info.full_name}\n'
            f'<b>Пользователь</b>\n'
            f'{mention_user}\nСлово: {text}',
            reply_markup=make_user_actions_log(
                message.from_user.id,
                message.chat.id
            )
        )


def register_filter_words_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_filter_words, subscribe_active=True,
        filter_words_active=True, filter_word_equal=True,
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    )
