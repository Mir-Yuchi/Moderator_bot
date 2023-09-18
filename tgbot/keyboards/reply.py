from aiogram.types import ReplyKeyboardMarkup

import tgbot.buttons.reply as rep_btn

SUPERUSER_START_COMMANDS = ReplyKeyboardMarkup([
    [rep_btn.UPDATE_TARIFF, rep_btn.TARIFF_LIST],
    [rep_btn.USERS_LIST, rep_btn.DELETE_USER],
    [rep_btn.USER_GROUPS, rep_btn.HELP_COMMANDS],
    [rep_btn.HOWTO_SETUP, rep_btn.FEATURES_DETAIL],
    [rep_btn.BOT_FEATURES]
], resize_keyboard=True)

USER_START_COMMANDS = ReplyKeyboardMarkup([
    [rep_btn.USER_GROUPS, rep_btn.HELP_COMMANDS],
    [rep_btn.HOWTO_SETUP, rep_btn.FEATURES_DETAIL],
    [rep_btn.BOT_FEATURES]
], resize_keyboard=True)

USER_GROUP_COMMANDS = ReplyKeyboardMarkup([
    [rep_btn.SUBSCRIBE_BUY, rep_btn.BOT_SETTINGS]
], resize_keyboard=True)

ADMIN_GROUP_COMMANDS = ReplyKeyboardMarkup([
    [rep_btn.BOT_SETTINGS]
], resize_keyboard=True)
