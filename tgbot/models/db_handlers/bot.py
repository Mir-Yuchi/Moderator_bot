from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.bot import UserTgGroupBot, RedisTgBotSettings


async def load_bot_settings_redis(pg_session: AsyncSession, redis: Redis):
    groups_bot: list[UserTgGroupBot] = await UserTgGroupBot.get_all(pg_session)
    for bot in groups_bot:
        redis_settings = RedisTgBotSettings(
            bot.user_id, bot.group_id, bot.bot_settings
        )
        await redis_settings.set_settings(redis)
