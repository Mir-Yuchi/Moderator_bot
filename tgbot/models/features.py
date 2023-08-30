from dataclasses import asdict

import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from . import BASE, AsyncBaseModelMixin
from tgbot.data.bot_features import FeaturesList
from tgbot.interfaces.features import BotFeatureInfo


class Features(BASE, AsyncBaseModelMixin):
    __tablename__ = 'features'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


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
    await session.execute(sa.delete(Features).where(
        Features.id.not_in(create_update_ids)
    ))
    await session.commit()
    if create_data:
        create_data = await Features.bulk_create(
            session,
            [asdict(obj.value.info.value) for obj in create_data]
        )
        features.extend(create_data)
    return features
