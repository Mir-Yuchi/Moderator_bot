from dataclasses import dataclass
from typing import Any

from aiogram.types import InlineKeyboardButton

from tgbot.interfaces.features import FeatureSettings


@dataclass
class FilterWordsSettings(FeatureSettings):
    words_list: list

    def make_inline_keyboard_buttons(
        self, settings: dict[Any]
    ) -> list[InlineKeyboardButton]:
        buttons = super().make_inline_keyboard_buttons(settings)
        buttons.append(InlineKeyboardButton(
            'Заменить список стоп слов ➕', callback_data='words_list__add'
        ))
        return buttons

    def features_text_dict(self, settings: dict[Any]) -> dict[str]:
        dict_ = super().features_text_dict(settings)
        words_list: list = settings['words_list']
        return dict_ | {
            'Список стоп слов': (
                ', '.join(words_list)
                if words_list else 'Пусто ✖️'
            )
        }
