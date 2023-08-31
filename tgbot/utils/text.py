from typing import Iterable

from tgbot.data.bot_features import FeaturesList
from tgbot.data.db_field_names import TARIFF_FIELD_NAMES


def numerate_iterable(iterable: Iterable, start: int = 1) -> tuple:
    for idx, value in enumerate(iterable, start=start):
        yield idx, value


def numerate_iterable_txt(iterable: Iterable) -> str:
    for idx, value in numerate_iterable(iterable):
        yield f'<strong>{idx}</strong>: {value}'


def mention_user_html(tg_id: int, full_name: str) -> str:
    return f'<a href="tg://user?id={tg_id}">{full_name}</a>'


def load_bot_feature_names() -> str:
    for idx, numerated_enum in numerate_iterable(
        FeaturesList.__members__.values(),
    ):
        yield f'<strong>{idx}: {numerated_enum.value.info.value.name}</strong>'


def bot_feature_detail_info() -> str:
    for feature in FeaturesList.__members__.values():
        yield (f'<strong>⚔️ {feature.value.info.value.name}</strong>\n'
               f'{feature.value.info.value.title}')


def confirm_create_tariff(
    tariff_name: str, limitation_days: int,
    groups_count: int, tariff_sum: int = 0,
    extra_txt: tuple = ()
) -> str:
    txt = extra_txt + (
        TARIFF_FIELD_NAMES['name'] + ': ' + tariff_name,
        TARIFF_FIELD_NAMES['limitation_days'] + ': ' +
        limitation_days.__str__(),
        TARIFF_FIELD_NAMES['groups_count'] + ': ' + groups_count.__str__(),
        TARIFF_FIELD_NAMES['sum'] + ': ' +
        ('Бесплатно 🆓' if not tariff_sum else tariff_sum.__str__() + '\u20BD')
    )
    return '\n'.join(txt)
