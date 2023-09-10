from aiogram import Dispatcher

from tgbot.handlers.groups.features.delete_meta import register_meta_handlers
from tgbot.handlers.groups.features.obscene_delete import (
    register_obscene_handlers
)


def register_all_features_handlers(dp: Dispatcher):
    register_meta_handlers(dp)
    register_obscene_handlers(dp)
