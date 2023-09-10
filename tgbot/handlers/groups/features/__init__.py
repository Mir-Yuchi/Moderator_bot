from aiogram import Dispatcher

from tgbot.handlers.groups.features.delete_meta import register_meta_handlers


def register_all_features_handlers(dp: Dispatcher):
    register_meta_handlers(dp)
