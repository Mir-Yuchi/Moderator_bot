from tgbot.filters.features.delete_meta import MetaDeleteActive
from tgbot.filters.features.obscene_delete import ObsceneDeleteActive


def register_all_features_filters(dp):
    dp.filters_factory.bind(MetaDeleteActive)
    dp.filters_factory.bind(ObsceneDeleteActive)
