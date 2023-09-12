import easyocr
from aiogram import Dispatcher
from aiogram.types import Message, ChatType, ContentType
from redis.asyncio import Redis

from tgbot.config import Config
from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings
from tgbot.utils.decorators import only_chat_users_handler
from tgbot.utils.file import detect_obvious_word, detect_obv_list_word


@only_chat_users_handler
async def check_media(message: Message):
    config: Config = message.bot['config']
    redis: Redis = message.bot['redis_db']
    settings = await RedisTgBotSettings(
        message.chat.id
    ).load_settings(redis)
    filter_settings = settings[FeaturesList.filter_words.name]
    silent_mode = settings[FeaturesList.silence_mode.name]['on']
    words = filter_settings['words_list']
    if message.photo:
        file = await message.bot.download_file_by_id(
            message.photo[-1].file_id
        )
    else:
        file = await message.bot.download_file_by_id(
            message.document.file_id
        )
    reader = easyocr.Reader(['ru'], False)
    text_list: list[str] = reader.readtext(
        file.read(), detail=False, paragraph=True
    )
    for text in text_list:
        text = text.lower().strip()
        check_word = detect_obvious_word(
            config.misc.OBSCENE_WORDS_FILE, text
        )
        check_word_filter = detect_obv_list_word(
            words, text
        )
        if check_word or check_word_filter:
            if not silent_mode:
                await message.reply('Кидать запрещённые картинки нельзя!')
            await message.bot.delete_message(
                message.chat.id,
                message.message_id
            )
            await message.bot.restrict_chat_member(
                message.chat.id,
                message.from_user.id,
                None,
                can_send_media_messages=False,
                can_send_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            )
            return


def register_media_handlers(dp: Dispatcher):
    dp.register_message_handler(
        check_media, subscribe_active=True,
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT]
    )
