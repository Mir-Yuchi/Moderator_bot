from aiogram import Dispatcher

from .entry import register_admin_entry_handlers


def register_admin_handlers(dp: Dispatcher):
    register_admin_entry_handlers(dp)
