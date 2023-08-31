from aiogram import Dispatcher

from tgbot.handlers.admin import register_admin_handlers
from tgbot.handlers.clients import register_all_client_handlers
from tgbot.handlers.echo import register_echo
from tgbot.handlers.groups import register_all_group_handlers


def register_all_handlers(dp: Dispatcher):
    register_admin_handlers(dp)
    register_all_client_handlers(dp)
    register_all_group_handlers(dp)
    register_echo(dp)
