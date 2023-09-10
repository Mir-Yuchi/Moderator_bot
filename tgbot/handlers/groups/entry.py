from datetime import datetime, timedelta

from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from redis.asyncio import Redis

from tgbot.config import Config
from tgbot.data.commands import Commands
from tgbot.models.admin import AdminGroupBot
from tgbot.models.bot import RedisTgBotSettings
from tgbot.models.client import BotClient, ClientSubscribe
from tgbot.models.tariffs import Tariff
from tgbot.utils.db import AsyncDbManager
from tgbot.utils.features import load_all_feature_settings


async def add_chat(message: Message):
    config: Config = message.bot['config']
    bot_admin_status = message.from_user.id in config.tg_bot.admin_ids
    settings = load_all_feature_settings()
    async with AsyncDbManager().db_session() as session:
        subscribe: ClientSubscribe | None = await ClientSubscribe.get_one(
            session, {'group_id': message.chat.id}
        )
        check_chat_admin = await AdminGroupBot.get_one(
            session, {'group_id': message.chat.id}
        )
        tariff: Tariff = await Tariff.get_one(session)
    if subscribe:
        if subscribe.active:
            await message.answer('Чат уже привязан')
            return
    if check_chat_admin:
        await message.answer('Чат уже привязан')
        return
    if bot_admin_status:
        async with AsyncDbManager().db_session() as session:
            await AdminGroupBot.create(session, {
                'admin_id': message.from_user.id,
                'group_id': message.chat.id,
                'bot_settings': settings
            })
    else:
        async with AsyncDbManager().db_session() as session:
            client: BotClient | None = await BotClient.get_one(
                session, {'tg_id': message.from_user.id}
            )
            if not client:
                await message.answer('Вы не являетесь пользователем бота')
                return
            if not subscribe:
                await ClientSubscribe.create(
                    session, {
                        'group_id': message.chat.id,
                        'client_id': message.from_user.id,
                        'tariff_id': tariff.id,
                        'expire_date': (
                            datetime.now() +
                            timedelta(config.misc.TARIFF_TRIAL_DAYS)
                        ),
                        'bot_settings': settings
                    })
                await message.bot.send_message(
                    message.from_user.id,
                    f'Вам предоставлена бесплатная подписка на '
                    f'{config.misc.TARIFF_TRIAL_DAYS} дней, дальше надо '
                    f'приобрести подписку'
                )
            else:
                await ClientSubscribe.update(
                    session, {'id': subscribe.id}, {'client_id': client.tg_id}
                )
                await message.bot.send_message(
                    message.from_user.id,
                    f'Бот привязан на ваш аккаунт, но подписка на нём '
                    f'просрочена, приобретайте подписку'
                )
                return
    redis: Redis = message.bot['redis_db']
    rdb_obj = RedisTgBotSettings(
        message.chat.id, settings
    )
    await rdb_obj.set_settings(redis)
    await message.answer('👌👌')


def register_entry_chat_handlers(dp: Dispatcher):
    dp.register_message_handler(
        add_chat, chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
        commands=[Commands.add.name]
    )
