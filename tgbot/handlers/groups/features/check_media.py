import pytesseract
from PIL import Image
from aiogram import Dispatcher
from aiogram.types import Message, ChatType, ContentType, ChatPermissions
from redis.asyncio import Redis

from tgbot.config import Config
from tgbot.data.bot_features import FeaturesList
from tgbot.models.bot import RedisTgBotSettings
from tgbot.utils.file import detect_obvious_word


async def check_media(message: Message):
    chat_admins = await message.chat.get_administrators()
    for admin in chat_admins:
        if admin.user.id == message.from_user.id:
            return
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
    img_text = pytesseract.image_to_string(Image.open(file), lang='rus')
    text_list: list[str] = img_text.replace('\n', ' ').split()
    for text in text_list:
        text = text.lower()
        check_word = detect_obvious_word(
            config.misc.OBSCENE_WORDS_FILE, text
        )
        if check_word or text in words:
            if not silent_mode:
                await message.reply('Кидать запрещённые картинки нельзя!')
            await message.bot.delete_message(
                message.chat.id,
                message.message_id
            )
            await message.bot.restrict_chat_member(
                message.chat.id,
                message.from_user.id,
                ChatPermissions(False, False, False, False, False, False,
                                False, False, False, False, False, False,
                                False, False, False)
            )
            return


def register_media_handlers(dp: Dispatcher):
    dp.register_message_handler(
        check_media, subscribe_active=True,
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT]
    )
