from aiogram import Dispatcher

from tgbot.handlers.admin.tariffs.create import register_tariff_create_handlers
from tgbot.handlers.admin.tariffs.delete import register_delete_tariff_handlers
from tgbot.handlers.admin.tariffs.list import register_tariff_list_handlers
from tgbot.handlers.admin.tariffs.update import register_tariff_update_handlers


def register_all_tariff_handlers(dp: Dispatcher):
    register_tariff_list_handlers(dp)
    register_tariff_create_handlers(dp)
    register_delete_tariff_handlers(dp)
    register_tariff_update_handlers(dp)
