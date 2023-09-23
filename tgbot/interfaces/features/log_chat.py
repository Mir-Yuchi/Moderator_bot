from dataclasses import dataclass
from typing import Any

from aiogram.types import InlineKeyboardButton

from tgbot.interfaces.features import FeatureSettings


@dataclass
class LogChatSettings(FeatureSettings):
    group_id: int | None = None

    def make_inline_keyboard_buttons(
        self, settings: dict[Any]
    ) -> list[InlineKeyboardButton]:
        kb_list = super().make_inline_keyboard_buttons(settings)
        kb_list.append(InlineKeyboardButton(
            'Удалить лог чат ➖',
            callback_data='log_chat__del'
        ))
        kb_list.append(InlineKeyboardButton(
            'Привязать лог чат ➕',
            callback_data='log_chat__add'
        ))
        return kb_list

    def features_text_dict(self, settings: dict[Any]) -> dict[str]:
        dict_ = super().features_text_dict(settings)
        group_id = settings['group_id']
        return dict_ | {
            '🆔 лог чата': group_id if group_id else 'Не привязано'
        }
