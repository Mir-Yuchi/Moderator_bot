from aiogram import Dispatcher

from tgbot.handlers.groups.entry import register_entry_chat_handlers


def register_all_group_handlers(dp: Dispatcher):
    register_entry_chat_handlers(dp)
