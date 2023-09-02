from aiogram.types import KeyboardButton, KeyboardButtonRequestChat

from tgbot.data.commands import ButtonCommands

UPDATE_TARIFF = KeyboardButton(ButtonCommands.update_tariff.value)
TARIFF_LIST = KeyboardButton(ButtonCommands.tariff_list.value)
USERS_LIST = KeyboardButton(ButtonCommands.users_list.value)
DELETE_USER = KeyboardButton(ButtonCommands.delete_users.value)
