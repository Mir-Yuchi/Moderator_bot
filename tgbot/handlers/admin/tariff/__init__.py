from aiogram import Dispatcher

from tgbot.handlers.admin.tariff.list import register_tariff_list_handlers
from tgbot.handlers.admin.tariff.update import register_tariff_update_handlers


def register_tariff_handlers(dp: Dispatcher):
    register_tariff_list_handlers(dp)
    register_tariff_update_handlers(dp)
