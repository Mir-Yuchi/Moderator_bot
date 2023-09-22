from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, ChatType, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from redis.asyncio import Redis

from tgbot.buttons.inline import CANCEL, BACK
from tgbot.config import Config
from tgbot.data.bot_features import FeaturesList
from tgbot.data.commands import ButtonCommands
from tgbot.interfaces.features import FeatureSettings
from tgbot.keyboards.inline import (
    make_features_inline_kb
)

from tgbot.keyboards.reply import (
    USER_START_COMMANDS, SUPERUSER_START_COMMANDS, ADMIN_GROUP_COMMANDS,
    USER_GROUP_COMMANDS,
)
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
    keyboard = make_features_inline_kb(group_id)
    keyboard.add(InlineKeyboardButton(
        CANCEL.text, callback_data=f'{group_id}__cancel'
    ))
    await message.answer(
        'Выберите фичу для настроек',
        reply_markup=keyboard,
    )


async def bot_settings_callback(callback: CallbackQuery, state: FSMContext):
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    config: Config = callback.bot['config']
    redis: Redis = callback.bot['redis_db']
    admin_status = callback.from_user.id in config.tg_bot.admin_ids
    group_id, feature_name = callback.data.split('__')
    group_id = int(group_id)
    redis_obj = RedisTgBotSettings(group_id)
    settings = await redis_obj.load_settings(redis)
    if feature_name == 'back':
        if admin_status:
            keyboard = ADMIN_GROUP_COMMANDS
        else:
            keyboard = USER_GROUP_COMMANDS
        await GroupsMenuState.group_actions.set()
        await state.update_data(choose_group=group_id)
        txt = ''
        for name, setting in settings.items():
            feature = getattr(FeaturesList, name).value
            feature_txt = f'<b>{feature.info.value.name}</b>\n'
            feature_settings_dict: dict = (
                feature.settings.value.features_text_dict(setting)
            )
            for key, value in feature_settings_dict.items():
                feature_txt += f'{key}: {value}\n'
            feature_txt += '\n'
            txt += feature_txt
        await callback.bot.send_message(
            callback.from_user.id,
            f'Ваши настройки чата\n\n{txt}\nВыберите действие',
            reply_markup=keyboard
        )
        return
    elif feature_name == 'cancel':
        await state.finish()
        await callback.bot.send_message(
            callback.from_user.id,
            'Отменено',
            reply_markup=(
                SUPERUSER_START_COMMANDS if admin_status
                else USER_START_COMMANDS
            )
        )
        return
    feature = getattr(FeaturesList, feature_name)
    feature_settings_obj: FeatureSettings = feature.value.settings.value
    await state.update_data(group_id=group_id, feature_settings=feature_name)
    feature_settings = settings[feature_name]
    keyboard = InlineKeyboardMarkup()
    buttons = feature_settings_obj.make_inline_keyboard_buttons(
        feature_settings
    )
    buttons.append(InlineKeyboardButton(
        BACK.text, callback_data=f'back')
    )
    for btn in buttons:
        keyboard.add(btn)
    keyboard.add(CANCEL)
    await FeatureSettingsState.set_settings.set()
    await callback.bot.send_message(
        callback.from_user.id,
        'Выберите действие',
        reply_markup=keyboard
    )


async def set_settings_callback(callback: CallbackQuery, state: FSMContext):
    config: Config = callback.bot['config']
    admin_status = callback.from_user.id in config.tg_bot.admin_ids
    redis: Redis = callback.bot['redis_db']
    async with state.proxy() as data:
        group_id = data.get('group_id')
        feature_name = data.get('feature_settings')
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    if callback.data == 'cancel':
        await state.finish()
        await callback.bot.send_message(
            callback.from_user.id,
            'Отменено',
            reply_markup=(
                SUPERUSER_START_COMMANDS if admin_status
                else USER_START_COMMANDS
            )
        )
        return
    elif callback.data == 'back':
        await state.finish()
        await FeatureSettingsState.feature_settings.set()
        keyboard = make_features_inline_kb(group_id)
        keyboard.add(CANCEL)
        await callback.bot.send_message(
            callback.from_user.id,
            'Выберите фичу для настроек',
            reply_markup=keyboard,
        )
        return
    async with AsyncDbManager().db_session() as session:
        if not admin_status:
            client_sub: ClientSubscribe = await ClientSubscribe.get_one(
                session,
                {'group_id': group_id, 'client_id': callback.from_user.id},
            )
        else:
            client_sub: AdminGroupBot = await AdminGroupBot.get_one(
                session,
                {'group_id': group_id, 'admin_id': callback.from_user.id}
            )
    feature_option_name, feature_option_value = callback.data.split('__')
    if feature_option_name == 'on':
        client_sub.bot_settings[feature_name][feature_option_name] = (
            True if feature_option_value == 'on' else False
        )
    elif feature_option_name == 'words_list':
        if feature_option_value == 'add':
            await callback.bot.send_message(
                callback.from_user.id,
                'Отлично! Введите стоп-слова разделённые через запятую'
            )
            await FeatureSettingsState.add_word_list.set()
        return
    else:
        client_sub.bot_settings[feature_name][feature_option_name] = (
            feature_option_value
        )
    await state.finish()
    rdb_obj = RedisTgBotSettings(group_id, client_sub.bot_settings)
    await rdb_obj.set_settings(redis)
    async with AsyncDbManager().db_session() as session:
        if not admin_status:
            await ClientSubscribe.update(
                session,
                {'group_id': group_id, 'client_id': callback.from_user.id},
                {'bot_settings': client_sub.bot_settings}
            )
        else:
            await AdminGroupBot.update(
                session,
                {'group_id': group_id, 'admin_id': callback.from_user.id},
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


async def add_word(message: Message, state: FSMContext):
    config: Config = message.bot['config']
    redis: Redis = message.bot['redis_db']
    async with state.proxy() as data:
        group_id = int(data.get('group_id'))
        feature_name = data.get('feature_settings')
    admin_status = message.from_user.id in config.tg_bot.admin_ids
    async with AsyncDbManager().db_session() as session:
        if not admin_status:
            client_sub: ClientSubscribe = await ClientSubscribe.get_one(
                session,
                {'group_id': group_id, 'client_id': message.from_user.id},
            )
        else:
            client_sub: AdminGroupBot = await AdminGroupBot.get_one(
                session,
                {'group_id': group_id, 'admin_id': message.from_user.id}
            )
    client_sub.bot_settings[feature_name]['words_list'] = (
        message.text.split(',')
    )
    rdb_obj = RedisTgBotSettings(group_id, client_sub.bot_settings)
    await rdb_obj.set_settings(redis)
    async with AsyncDbManager().db_session() as session:
        if not admin_status:
            await ClientSubscribe.update(
                session,
                {'group_id': group_id, 'client_id': message.from_user.id},
                {'bot_settings': client_sub.bot_settings}
            )
        else:
            await AdminGroupBot.update(
                session,
                {'group_id': group_id, 'admin_id': message.from_user.id},
                {'bot_settings': client_sub.bot_settings}
            )
    await state.finish()
    await message.answer(
        'Успешно заменил список',
        reply_markup=(
            SUPERUSER_START_COMMANDS if admin_status
            else USER_START_COMMANDS
        )
    )


def register_features_update_handlers(dp: Dispatcher):
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
    dp.register_message_handler(
        add_word, chat_type=ChatType.PRIVATE,
        state=FeatureSettingsState.add_word_list
    )
