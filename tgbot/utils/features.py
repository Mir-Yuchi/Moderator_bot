from tgbot.data.bot_features import FeaturesList


def load_all_feature_settings() -> dict:
    settings = {}
    for feature_name, feature_obj in FeaturesList.__members__.items():
        f_settings = feature_obj.value.settings.value.to_dict()
        settings[feature_name] = f_settings
    return settings
