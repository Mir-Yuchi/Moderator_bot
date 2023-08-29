from typing import Iterable

from tgbot.data.bot_features import FeaturesList


def numerate_iterable(iterable: Iterable, start: int = 1):
    for idx, value in enumerate(iterable, start=start):
        yield idx, value


def load_bot_feature_names():
    for idx, numerated_enum in numerate_iterable(
        FeaturesList.__members__.values(),
    ):
        yield f'<strong>{idx}: {numerated_enum.value.info.value.name}</strong>'


def bot_feature_detail_info():
    for feature in FeaturesList.__members__.values():
        yield (f'<strong>⚔️ {feature.value.info.value.name}</strong>\n'
               f'{feature.value.info.value.title}')
