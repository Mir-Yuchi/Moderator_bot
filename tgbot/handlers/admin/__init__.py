from aiogram import Dispatcher

from .clients import register_all_admin_client_handlers
from .entry import register_admin_entry_handlers
from .tariff import register_tariff_handlers


def register_admin_handlers(dp: Dispatcher):
    register_admin_entry_handlers(dp)
    register_all_admin_client_handlers(dp)
    register_tariff_handlers(dp)
