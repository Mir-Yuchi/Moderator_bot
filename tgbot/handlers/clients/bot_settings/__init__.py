from aiogram import Dispatcher

from tgbot.handlers.clients.bot_settings.update import (
    register_features_update_handlers
)


def register_all_bot_settings_handlers(dp: Dispatcher):
    register_features_update_handlers(dp)
