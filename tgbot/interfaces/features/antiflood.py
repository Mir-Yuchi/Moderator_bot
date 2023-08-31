from dataclasses import dataclass, asdict
from enum import Enum

from tgbot.interfaces.features import FeatureSettings


class WorkModeChoice(Enum):
    strict = 'Строгий режим'
    less_strict = 'Менее строгий режим'


@dataclass
class AntiFloodSettings(FeatureSettings):
    work_mode: WorkModeChoice

    def to_dict(self):
        return {
            'work_mode': self.work_mode.name
        }
