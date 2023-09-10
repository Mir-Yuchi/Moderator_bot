from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.admin import AdminGroupBot
from tgbot.models.bot import RedisTgBotSettings
from tgbot.models.client import ClientSubscribe
from tgbot.utils.db import AsyncDbManager
from tgbot.utils.features import load_all_feature_settings


async def check_new_features(
    subscribe: ClientSubscribe | AdminGroupBot
) -> ClientSubscribe | AdminGroupBot:
    settings = load_all_feature_settings()
    for key, value in settings.items():
        if key not in subscribe.bot_settings:
            subscribe.bot_settings[key] = value
    for key in list(subscribe.bot_settings.keys()):
        if key not in settings:
            subscribe.bot_settings.pop(key)
    async with AsyncDbManager().db_session() as session:
        if isinstance(subscribe, ClientSubscribe):
            return await ClientSubscribe.update(
                session, {'id': subscribe.id},
                {'bot_settings': subscribe.bot_settings}
            )
        else:
            return await AdminGroupBot.update(
                session, {'group_id': subscribe.group_id},
                {'bot_settings': subscribe.bot_settings}
            )


async def load_bot_settings_redis(pg_session: AsyncSession, redis: Redis):
    groups_bot: list[ClientSubscribe] = (
        await ClientSubscribe.get_all(pg_session, {'active': True})
    )
    admins_bot: list[AdminGroupBot] = (
        await AdminGroupBot.get_all(pg_session)
    )
    for bot in groups_bot:
        check_feature = await check_new_features(bot)
        redis_settings = RedisTgBotSettings(
            bot.group_id, check_feature.bot_settings
        )
        await redis_settings.set_settings(redis)
    for bot2 in admins_bot:
        check_feature = await check_new_features(bot2)
        redis_settings = RedisTgBotSettings(
            bot2.group_id, check_feature.bot_settings
        )
        await redis_settings.set_settings(redis)
