from aiogram import Dispatcher

from tgbot.handlers.groups.chat_admin_commands import (
    register_chat_admin_commands
)
from tgbot.handlers.groups.entry import register_entry_chat_handlers
from tgbot.handlers.groups.features import register_all_features_handlers


def register_all_group_handlers(dp: Dispatcher):
    register_chat_admin_commands(dp)
    register_entry_chat_handlers(dp)
    register_all_features_handlers(dp)
