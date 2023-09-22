from typing import Any

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.buttons.inline import YES, NO, BACK
from tgbot.data.bot_features import FeaturesList
from tgbot.models.admin import AdminGroupBot
from tgbot.models.client import BotClient, ClientSubscribe
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


def make_client_inline_kb(clients: list[BotClient]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for user in clients:
        btn = InlineKeyboardButton(
            user.full_name, callback_data=user.tg_id.__str__()
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


async def make_groups_inline_kb(
    bot: Bot,
    groups: list[AdminGroupBot | ClientSubscribe]
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for group in groups:
        chat = await bot.get_chat(group.group_id)
        btn = InlineKeyboardButton(chat.full_name, callback_data=str(chat.id))
        keyboard.add(btn)
    keyboard.add(BACK)
    return keyboard


def make_features_inline_kb(group_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for feature_obj_name, feature_obj in FeaturesList.__members__.items():
        feature_name = feature_obj.value.info.value.name
        keyboard.add(InlineKeyboardButton(
            feature_name, callback_data=f'{group_id}__{feature_obj_name}'
        ))
    keyboard.add(InlineKeyboardButton(
        BACK.text, callback_data=f'{group_id}__back'
    ))
    return keyboard


def make_enumerate_inline_kb(fields: list[Any]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for idx, value in enumerate(fields):
        keyboard.add(InlineKeyboardButton(
            value, callback_data=idx.__str__()
        ))
    return keyboard
