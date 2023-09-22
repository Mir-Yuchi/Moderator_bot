from aiogram.types import KeyboardButton, KeyboardButtonRequestChat

from tgbot.data.commands import ButtonCommands

UPDATE_TARIFF = KeyboardButton(ButtonCommands.update_tariff.value)
TARIFF_LIST = KeyboardButton(ButtonCommands.tariff_list.value)
USERS_LIST = KeyboardButton(ButtonCommands.users_list.value)
DELETE_USER = KeyboardButton(ButtonCommands.delete_users.value)
USER_GROUPS = KeyboardButton(ButtonCommands.my_groups.value)
SUBSCRIBE_BUY = KeyboardButton(ButtonCommands.buy_subscribe.value)
BOT_SETTINGS = KeyboardButton(ButtonCommands.bot_settings.value)
HELP_COMMANDS = KeyboardButton(ButtonCommands.help_commands.value)
HOWTO_SETUP = KeyboardButton(ButtonCommands.howto_setup.value)
FEATURES_DETAIL = KeyboardButton(ButtonCommands.features_detail.value)
BOT_FEATURES = KeyboardButton(ButtonCommands.bot_features.value)
BACK_BTN = KeyboardButton(ButtonCommands.back.value)
