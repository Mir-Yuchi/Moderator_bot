from aiogram import Dispatcher

from .entry import register_admin_entry_handlers
from .tariffs import register_all_tariff_handlers


def register_admin_handlers(dp: Dispatcher):
    register_admin_entry_handlers(dp)
    register_all_tariff_handlers(dp)
