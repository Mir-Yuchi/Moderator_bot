import asyncio

from redis.asyncio import Redis

from tgbot.models.bot import RedisTgBotSettings
from tgbot.models.client import ClientSubscribe
from tgbot.utils.db import AsyncDbManager


async def on_exit_reset_cache(redis: Redis):
    async with AsyncDbManager().db_session() as session:
        subscribes: list[ClientSubscribe] = (
            await ClientSubscribe.get_all(session)
        )
    for subscribe in subscribes:
        settings = RedisTgBotSettings(subscribe.group_id)
        await redis.delete(settings.db_settings_key)


async def daily_check_user_subscribe(redis: Redis, db_dsn: str):
    async with AsyncDbManager(db_dsn).db_session() as session:
        subscribes: list[ClientSubscribe] = (
            await ClientSubscribe.get_all(session, {'active': True})
        )
    for subscribe in subscribes:
        settings = RedisTgBotSettings(subscribe.group_id)
        if subscribe.expired():
            async with AsyncDbManager(db_dsn).db_session() as session:
                await ClientSubscribe.update(
                    session, {'id': subscribe.id},
                    {'active': False}
                )
            await redis.delete(settings.db_settings_key)
    await asyncio.sleep(72000)
    await daily_check_user_subscribe(redis, db_dsn)
