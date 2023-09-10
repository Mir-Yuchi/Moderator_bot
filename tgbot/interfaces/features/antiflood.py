from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any

from aiogram.types import InlineKeyboardButton

from tgbot.interfaces.features import FeatureSettings


class WorkModeChoice(Enum):
    strict = 'Строгий режим'
    less_strict = 'Менее строгий режим'


@dataclass
class AntiFloodSettings(FeatureSettings):
    work_mode: WorkModeChoice

    def features_text_dict(self, settings: dict[Any]):
        data = super().features_text_dict(settings)
        work_mode = settings['work_mode']
        mode = getattr(WorkModeChoice, work_mode)
        return data | {
            'Режим работы 🛠️': mode.value
        }

    def to_dict(self):
        data = super().to_dict()
        return data | {
            'work_mode': self.work_mode.name
        }

    def set_settings(self, setting_name: str, setting_value: str):
        setting = getattr(self, setting_name)
        if isinstance(setting, WorkModeChoice):
            settings: WorkModeChoice = getattr(WorkModeChoice, setting_value)
            self.work_mode = settings

    def make_inline_keyboard_buttons(
        self, settings: dict[Any]
    ) -> list[InlineKeyboardButton]:
        buttons = super().make_inline_keyboard_buttons(settings)
        if settings['work_mode'] == WorkModeChoice.strict.name:
            buttons.append(
                InlineKeyboardButton(
                    'Включить ' + WorkModeChoice.less_strict.value,
                    callback_data=f'work_mode__'
                                  f'{WorkModeChoice.less_strict.name}'
                )
            )
        else:
            buttons.append(
                InlineKeyboardButton(
                    'Включить ' + WorkModeChoice.strict.value,
                    callback_data=f'work_mode__{WorkModeChoice.strict.name}'
                )
            )
        return buttons
