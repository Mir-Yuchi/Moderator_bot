from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.bot_features import FeaturesList
from tgbot.interfaces.features import BotFeatureInfo
from tgbot.models.features import Features
from tgbot.models.tariffs import TariffFeature


async def define_initial_features_data(
    session: AsyncSession
) -> list[Features]:
    features: list[Features] = await Features.get_all(session)
    real_features = list(FeaturesList.__members__.values())
    create_data = []
    create_update_ids = []
    for idx, feature_obj in enumerate(real_features):
        feature_info_obj: BotFeatureInfo = feature_obj.value.info.value
        for feature_db_obj in features:
            if feature_info_obj.id == feature_db_obj.id:
                feature_db_obj.name = feature_info_obj.name
                feature_db_obj.title = feature_info_obj.title
                create_update_ids.append(feature_info_obj.id)
                session.add(feature_db_obj)
                break
        else:
            create_update_ids.append(feature_obj.value.info.value.id)
            create_data.append(feature_obj)
    await TariffFeature.delete_by_id_in(
        session, create_update_ids, 'feature_id', True
    )
    await Features.delete_by_id_in(session, create_update_ids, 'id', True)
    if create_data:
        create_data = await Features.bulk_create(
            session,
            [asdict(obj.value.info.value) for obj in create_data]
        )
        features.extend(create_data)
    return features
