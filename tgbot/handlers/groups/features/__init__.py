from aiogram import Dispatcher

from tgbot.handlers.groups.features.check_media import register_media_handlers
from tgbot.handlers.groups.features.delete_meta import register_meta_handlers
from tgbot.handlers.groups.features.filter_words import (
    register_filter_words_handlers
)
from tgbot.handlers.groups.features.log_chat import register_log_chat_handlers
from tgbot.handlers.groups.features.obscene_delete import (
    register_obscene_handlers
)


def register_all_features_handlers(dp: Dispatcher):
    register_meta_handlers(dp)
    register_filter_words_handlers(dp)
    register_obscene_handlers(dp)
    register_media_handlers(dp)
    register_log_chat_handlers(dp)
