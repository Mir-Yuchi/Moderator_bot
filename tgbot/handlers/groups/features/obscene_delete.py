from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from redis.asyncio import Redis

from tgbot.config import Config
from tgbot.data.bot_features import FeaturesList
from tgbot.keyboards.inline import make_user_actions_log
from tgbot.models.bot import RedisTgBotSettings
from tgbot.utils.decorators import only_chat_users_handler
from tgbot.utils.file import detect_obvious_word
from tgbot.utils.text import replace_word_letters, mention_user_html


@only_chat_users_handler
async def delete_obscene(message: Message):
    config: Config = message.bot['config']
    redis: Redis = message.bot['redis_db']
    settings = await RedisTgBotSettings(
        message.chat.id
    ).load_settings(redis)
    silent_mode = settings[FeaturesList.silence_mode.name]['on']
    phrase = replace_word_letters(message.text.lower().replace(' ', ''))
    check_word = detect_obvious_word(config.misc.OBSCENE_WORDS_FILE, phrase)
    if check_word:
        if not silent_mode:
            await message.reply('Маты запрещены в чате 👮🏻')
        await message.delete()
        log_chat_settings = settings[FeaturesList.log_chat.name]
        chat_log_id = log_chat_settings['group_id']
        if log_chat_settings['on'] and chat_log_id:
            chat_info = await message.bot.get_chat(message.chat.id)
            mention_user = mention_user_html(
                message.from_user.id, message.from_user.full_name
            )
            await message.bot.send_message(
                chat_log_id,
                f'<b>РЕПОРТ ПОЛЬЗОВАТЕЛЯ ЗА ИСПОЛЬЗОВАНИЕ МАТА</b>\n'
                f'<b>ЧАТ</b>\n🆔: {chat_info.id}\n'
                f'Название: {chat_info.full_name}\n'
                f'<b>Пользователь</b>\n'
                f'{mention_user}\nСлово: {check_word}',
                reply_markup=make_user_actions_log(
                    message.from_user.id,
                    message.chat.id
                )
            )


def register_obscene_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_obscene, subscribe_active=True,
        delete_obscene_active=True,
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    )
