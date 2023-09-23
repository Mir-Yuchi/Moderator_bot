from tgbot.filters.features.delete_meta import MetaDeleteActive
from tgbot.filters.features.filter_words import (
    FilterWordsActive,
    FilterWordEqual
)
from tgbot.filters.features.media import MediaActive
from tgbot.filters.features.obscene_delete import ObsceneDeleteActive


def register_all_features_filters(dp):
    dp.filters_factory.bind(MetaDeleteActive)
    dp.filters_factory.bind(ObsceneDeleteActive)
    dp.filters_factory.bind(FilterWordsActive)
    dp.filters_factory.bind(FilterWordEqual)
    dp.filters_factory.bind(MediaActive)
