from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.admin import AdminGroupBot
from tgbot.models.bot import RedisTgBotSettings
from tgbot.models.client import ClientSubscribe


async def load_bot_settings_redis(pg_session: AsyncSession, redis: Redis):
    groups_bot: list[ClientSubscribe] = (
        await ClientSubscribe.get_all(pg_session, {'active': True})
    )
    admins_bot: list[AdminGroupBot] = (
        await AdminGroupBot.get_all(pg_session)
    )
    for bot in groups_bot:
        redis_settings = RedisTgBotSettings(
            bot.group_id, bot.bot_settings
        )
        await redis_settings.set_settings(redis)
    for bot2 in admins_bot:
        redis_settings = RedisTgBotSettings(
            bot2.group_id, bot2.bot_settings
        )
        await redis_settings.set_settings(redis)
