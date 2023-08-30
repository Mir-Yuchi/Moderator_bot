from aiogram.types import KeyboardButton

from tgbot.data.commands import ButtonCommands

ADD_TARIFF = KeyboardButton(ButtonCommands.add_tariff.value)
DELETE_TARIFF = KeyboardButton(ButtonCommands.del_tariff.value)
UPDATE_TARIFF = KeyboardButton(ButtonCommands.update_tariff.value)
TARIFF_LIST = KeyboardButton(ButtonCommands.tariff_list.value)
