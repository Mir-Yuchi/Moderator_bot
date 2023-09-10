from dataclasses import dataclass, asdict
from typing import Any

from aiogram.types import InlineKeyboardButton


@dataclass
class BotFeatureInfo:
    name: str
    title: str


@dataclass
class FeatureSettings:
    on: bool

    def to_dict(self):
        return asdict(self)

    def make_inline_keyboard_buttons(
        self, settings: dict[Any]
    ) -> list[InlineKeyboardButton]:
        return [InlineKeyboardButton(
            'Выключить фичу ❌' if settings['on'] else 'Включить фичу ✅',
            callback_data='on__off' if settings['on'] else 'on__on'
        )]

    def features_text_dict(self, settings: dict[Any]) -> dict[str]:
        return {
            'Режим': f'{"Включено ✅" if settings["on"] else "Выключено ❌"}'
        }
