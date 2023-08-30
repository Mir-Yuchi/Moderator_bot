from aiogram.types import ReplyKeyboardMarkup

import tgbot.buttons.reply as rep_btn

SUPERUSER_START_COMMANDS = ReplyKeyboardMarkup([
    [rep_btn.ADD_TARIFF, rep_btn.DELETE_TARIFF],
    {rep_btn.UPDATE_TARIFF, rep_btn.TARIFF_LIST}
], resize_keyboard=True)
