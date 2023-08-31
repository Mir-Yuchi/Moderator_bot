from tgbot.data.bot_features import FeaturesList
from tgbot.models.features import Features
from tgbot.models.tariffs import TariffFeature


def load_all_feature_settings() -> dict:
    settings = {}
    for feature_name, feature_obj in FeaturesList.__members__.items():
        f_settings = feature_obj.value.settings.value.to_dict()
        settings[feature_name] = f_settings
    return settings


def load_feature_settings_by_id(features_db: list[TariffFeature | Features]):
    settings = {}
    for feature_db_obj in features_db:
        if isinstance(feature_db_obj, TariffFeature):
            search_id = feature_db_obj.feature_id
        else:
            search_id = Features.id
        for feature_name, feature_obj in FeaturesList.__members__.items():
            if feature_obj.value.info.value.id == search_id:
                settings[feature_name] = (
                    feature_obj.value.settings.value.to_dict()
                )
                break
    return settings
