from typing import Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.buttons.inline import YES, NO
from tgbot.models.tariffs import Tariff


def yes_or_no() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.row(YES, NO)
    return keyboard


def make_tariff_inline_kb(tariffs: list[Tariff]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for tariff in tariffs:
        btn = InlineKeyboardButton(
            tariff.name, callback_data=tariff.id.__str__()
        )
        keyboard.add(btn)
    return keyboard


def make_inline_kb_from_dict(
    dict_: dict[Any], callback_key: bool = False
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for key, value in dict_.items():
        if callback_key:
            keyboard.add(InlineKeyboardButton(
                value.__str__(), callback_data=key.__str__()
            ))
        else:
            keyboard.add(InlineKeyboardButton(
                key.__str__(), callback_data=value.__str__()
            ))
    return keyboard
