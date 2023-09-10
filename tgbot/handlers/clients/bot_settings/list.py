from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, ChatType, CallbackQuery,
    InlineKeyboardMarkup
)
from redis.asyncio import Redis

from tgbot.config import Config
from tgbot.data.bot_features import FeaturesList
from tgbot.data.commands import ButtonCommands
from tgbot.interfaces.features import FeatureSettings
from tgbot.keyboards.inline import make_features_inline_kb
from tgbot.keyboards.reply import USER_START_COMMANDS, SUPERUSER_START_COMMANDS
from tgbot.misc.states import GroupsMenuState, FeatureSettingsState
from tgbot.models.admin import AdminGroupBot
from tgbot.models.bot import RedisTgBotSettings
from tgbot.models.client import ClientSubscribe
from tgbot.utils.db import AsyncDbManager


async def bot_settings(message: Message, state: FSMContext):
    async with state.proxy() as data:
        group_id = int(data.get('choose_group'))
    await state.finish()
    await FeatureSettingsState.feature_settings.set()
    await message.answer(
        'Выберите фичу для настроек',
        reply_markup=make_features_inline_kb(group_id)
    )


async def bot_settings_callback(callback: CallbackQuery, state: FSMContext):
    redis: Redis = callback.bot['redis_db']
    group_id, feature_name = callback.data.split('__')
    feature = getattr(FeaturesList, feature_name)
    feature_settings_obj: FeatureSettings = feature.value.settings.value
    await state.update_data(group_id=group_id, feature_settings=feature_name)
    rdb_settings = await RedisTgBotSettings(group_id).load_settings(redis)
    feature_settings = rdb_settings[feature_name]
    txt = (
        f'Ваши настройки {feature.value.info.value.name}',
        '\n\n'.join(map(
            lambda tup: f'{tup[0]}: {tup[1]}',
            feature_settings_obj.features_text_dict(feature_settings).items()
        )),
        'Выберите действие'
    )
    keyboard = InlineKeyboardMarkup()
    buttons = feature_settings_obj.make_inline_keyboard_buttons(
        feature_settings
    )
    for btn in buttons:
        keyboard.add(btn)
    await FeatureSettingsState.set_settings.set()
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await callback.bot.send_message(
        callback.from_user.id,
        '\n\n'.join(txt),
        reply_markup=keyboard
    )


async def set_settings_callback(callback: CallbackQuery, state: FSMContext):
    config: Config = callback.bot['config']
    admin_status = callback.from_user.id in config.tg_bot.admin_ids
    async with state.proxy() as data:
        feature_name = data.get('feature_settings')
        group_id = int(data.get('group_id'))
    await state.finish()
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    async with AsyncDbManager().db_session() as session:
        if not admin_status:
            client_sub: ClientSubscribe = await ClientSubscribe.get_one(
                session,
                {'group_id': group_id, 'client_id': callback.from_user.id},
            )
            if client_sub.expired():
                await callback.bot.send_message(
                    callback.from_user.id,
                    'У вас нет подписки, сначала продлите подписку.',
                    reply_markup=USER_START_COMMANDS
                )
                return
        else:
            client_sub: AdminGroupBot = await AdminGroupBot.get_one(
                session,
                {'group_id': group_id, 'admin_id': callback.from_user.id}
            )
    split = callback.data.split('__')
    redis: Redis = callback.bot['redis_db']
    feature_option_name, feature_option_value = split
    if feature_option_name == 'on':
        client_sub.bot_settings[feature_name][feature_option_name] = (
            True if feature_option_value == 'on' else False
        )
    else:
        client_sub.bot_settings[feature_name][feature_option_name] = (
            feature_option_value
        )
    rdb_obj = RedisTgBotSettings(group_id, client_sub.bot_settings)
    await rdb_obj.set_settings(redis)
    async with AsyncDbManager().db_session() as session:
        await ClientSubscribe.update(
            session,
            {'group_id': group_id, 'client_id': callback.from_user.id},
            {'bot_settings': client_sub.bot_settings}
        )
    await callback.bot.send_message(
        callback.from_user.id,
        'Успешно применил настройки',
        reply_markup=(
            SUPERUSER_START_COMMANDS if admin_status
            else USER_START_COMMANDS
        )
    )


def register_features_list_handlers(dp: Dispatcher):
    dp.register_message_handler(
        bot_settings, chat_type=ChatType.PRIVATE,
        state=GroupsMenuState.group_actions,
        text=ButtonCommands.bot_settings.value
    )
    dp.register_callback_query_handler(
        bot_settings_callback, chat_type=ChatType.PRIVATE,
        state=FeatureSettingsState.feature_settings,
    )
    dp.register_callback_query_handler(
        set_settings_callback, chat_type=ChatType.PRIVATE,
        state=FeatureSettingsState.set_settings,
    )
