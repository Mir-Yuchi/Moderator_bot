from aiogram import Dispatcher

from tgbot.handlers.clients.bot_settings.list import (
    register_features_list_handlers
)

from tgbot.handlers.clients.bot_settings.meta_info import (
    register_meta_info_handlers
)


def register_all_bot_settings_handlers(dp: Dispatcher):
    register_features_list_handlers(dp)
    register_meta_info_handlers(dp)
