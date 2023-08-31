from aiogram import Dispatcher

from .delete import register_client_delete_handlers
from .list import register_client_list_handlers


def register_all_admin_client_handlers(dp: Dispatcher):
    register_client_list_handlers(dp)
    register_client_delete_handlers(dp)
