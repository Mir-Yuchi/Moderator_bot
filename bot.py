import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from redis.asyncio import Redis

from tgbot.config import load_config, load_redis_config
from tgbot.filters import register_all_filters
from tgbot.handlers import register_all_handlers
from tgbot.middleware.antiflood import AntiSpamMiddleware
from tgbot.models.db_handlers.bot import load_bot_settings_redis
from tgbot.models.tariffs import Tariff
from tgbot.tasks.daily import daily_check_user_subscribe, on_exit_reset_cache
from tgbot.utils.bot import load_bot_commands
from tgbot.utils.db import AsyncDbManager

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - '
               u'%(name)s - %(message)s',
    )
    logger.info('Starting bot')
    config = load_config('.env')
    redis_conf = load_redis_config('.env')
    storage = RedisStorage2(
        redis_conf.host, redis_conf.port, redis_conf.database
    ) if config.tg_bot.use_redis else MemoryStorage()
    redis_engine = Redis(
        host=redis_conf.host,
        port=redis_conf.port,
        db=redis_conf.database,
        decode_responses=True
    )
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    await bot.set_my_commands(load_bot_commands())
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    bot['redis_db'] = redis_engine
    async with AsyncDbManager(
        config.db.async_url()
    ).db_session() as db_session:
        tariff = await Tariff.get_one(db_session)
        if not tariff:
            await Tariff.create(db_session, {
                'name': 'PREMIUM',
                'sum': 1000,
                'limitation_days': 30,
            })
        await load_bot_settings_redis(db_session, redis_engine)
    dp.middleware.setup(AntiSpamMiddleware())
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        # for admin in config.tg_bot.admin_ids:
        #     await bot.send_message(admin, 'Бот запустился')
        await asyncio.gather(
            daily_check_user_subscribe(redis_engine, config.db.async_url()),
            dp.start_polling()
        )
    finally:
        # for admin in config.tg_bot.admin_ids:
        #     await bot.send_message(admin, 'Бот отановился')
        await on_exit_reset_cache(redis_engine)
        logger.info('CACHE RESET')
        await redis_engine.close()
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()
        logger.info('BOT SESSION CLOSE')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
