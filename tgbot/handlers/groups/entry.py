from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from redis.asyncio import Redis

from tgbot.config import Config
from tgbot.data.commands import Commands
from tgbot.models.bot import UserTgGroupBot, RedisTgBotSettings
from tgbot.models.client import BotClient, ClientSubscribe
from tgbot.models.tariffs import Tariff, TariffFeature
from tgbot.tasks.message import delete_message_after_time
from tgbot.utils.db import AsyncDbManager
from tgbot.utils.features import (
    load_all_feature_settings,
    load_feature_settings_by_id
)


async def add_chat(message: Message):
    async with AsyncDbManager().db_session() as session:
        client: BotClient | None = await BotClient.get_one(
            session, {'tg_id': message.from_user.id}
        )
    if not client:
        await message.bot.delete_message(
            message.chat.id,
            message.message_id
        )
        msg = await message.answer('Вы не являетесь пользователем бота')
        await delete_message_after_time(
            message.bot, message.chat.id, msg.message_id, 3
        )
        return
    async with AsyncDbManager().db_session() as session:
        group = await UserTgGroupBot.get_one(
            session, {'group_id': message.chat.id}
        )
        tariffs: list[Tariff] = await Tariff.get_all(session)
        subscribe: ClientSubscribe = await ClientSubscribe.get_one(
            session, {'client_id': message.from_user.id}
        )
    if group:
        msg = await message.answer('Группа уже привязана')
        await delete_message_after_time(
            msg.bot, msg.chat.id, msg.message_id, 3
        )
        return
    if not tariffs:
        msg = await message.answer('Нет подходящих тарифов для подписки')
        await delete_message_after_time(
            msg.bot, msg.chat.id, msg.message_id, 3
        )
        return
    config: Config = message.bot['config']
    bot_admin_status = message.from_user.id in config.tg_bot.admin_ids
    if bot_admin_status:
        settings = load_all_feature_settings()
    else:
        if not subscribe:
            msg = await message.answer('У вас нет подписки')
            await delete_message_after_time(
                msg.bot, msg.chat.id, msg.message_id, 3
            )
            return
        user_tariff = None
        for tariff in tariffs:
            if tariff.id == subscribe.tariff_id:
                user_tariff = tariff
                break
        else:
            msg = await message.answer(
                'Ваш тариф не найден, купите подписку по другому тарифу'
            )
            await delete_message_after_time(
                msg.bot, msg.chat.id, msg.message_id, 3
            )
            return
        if subscribe.expired(user_tariff.limitation_days):
            msg = await message.answer('Просроченная подписка')
            await delete_message_after_time(
                msg.bot, msg.chat.id, msg.message_id, 3
            )
            return
        async with AsyncDbManager().db_session() as session:
            features = await TariffFeature.get_all(
                session, {'tariff_id': subscribe.tariff_id}
            )
        settings = load_feature_settings_by_id(features)
    await UserTgGroupBot.create(
        session,
        {
            'group_id': message.chat.id,
            'user_id': client.tg_id,
            'bot_settings': settings
        }
    )
    redis: Redis = message.bot['redis_db']
    rdb_obj = RedisTgBotSettings(client.tg_id, message.chat.id, settings)
    await rdb_obj.set_settings(redis)
    msg = await message.answer('👌👌')
    await delete_message_after_time(
        message.bot, msg.chat.id, msg.message_id, 3
    )
    await delete_message_after_time(
        message.bot, message.chat.id, message.message_id, 3
    )


def register_entry_chat_handlers(dp: Dispatcher):
    dp.register_message_handler(
        add_chat, chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
        commands=[Commands.add.name]
    )
