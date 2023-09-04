from aiogram import Dispatcher

from tgbot.handlers.clients.entry import register_entry_handlers
from tgbot.handlers.clients.tariff_payments import register_payment_handlers


def register_all_client_handlers(dp: Dispatcher):
    register_entry_handlers(dp)
    register_payment_handlers(dp)
