from tgbot.filters.features.delete_meta import MetaDeleteActive


def register_all_features_filters(dp):
    dp.filters_factory.bind(MetaDeleteActive)
