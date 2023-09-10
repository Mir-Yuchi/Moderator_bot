from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType, CallbackQuery
from redis.asyncio import Redis

from tgbot.data.commands import ButtonCommands
from tgbot.keyboards.inline import make_client_inline_kb, yes_or_no
from tgbot.misc.states import DeleteUserState
from tgbot.models.bot import RedisTgBotSettings
from tgbot.models.client import BotClient, ClientSubscribe
from tgbot.utils.db import AsyncDbManager


async def delete_user_command(message: Message):
    async with AsyncDbManager().db_session() as session:
        clients = await BotClient.get_all(session)
    if not clients:
        await message.answer('пользователей нет')
        return
    keyboard = make_client_inline_kb(clients)
    await message.answer(
        'Отлично! Выберите кого удалить',
        reply_markup=keyboard
    )
    await DeleteUserState.callback.set()


async def delete_user_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(callback=int(callback.data))
    await DeleteUserState.confirm.set()
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await callback.bot.send_message(
        callback.from_user.id,
        'Вы точно хотите удалить пользователя??',
        reply_markup=yes_or_no()
    )


async def confirm_delete_user_callback(
    callback: CallbackQuery, state: FSMContext
):
    redis: Redis = callback.bot['redis_db']
    match callback.data:
        case 'yes':
            async with state.proxy() as data:
                field_id = data.get('callback')
            async with AsyncDbManager().db_session() as session:
                user_subs: list[ClientSubscribe] = (
                    await ClientSubscribe.get_all(
                        session, {'client_id': field_id}
                    )
                )
                await ClientSubscribe.delete(session, {'client_id': field_id})
                await BotClient.delete(session, {'tg_id': field_id})
            for subscribe in user_subs:
                redis_db_obj = RedisTgBotSettings(
                    subscribe.group_id,
                    subscribe.bot_settings
                )
                await redis.delete(redis_db_obj.db_settings_key)
            await callback.bot.send_message(
                callback.from_user.id,
                'Успешно удалил пользователя'
            )
        case _:
            await callback.bot.send_message(
                callback.from_user.id,
                'Отменено ❌'
            )
    await state.finish()
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )


def register_client_delete_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_user_command, chat_type=ChatType.PRIVATE,
        text=ButtonCommands.delete_users.value, is_superuser=True,
    )
    dp.register_callback_query_handler(
        delete_user_callback, chat_type=ChatType.PRIVATE,
        state=DeleteUserState.callback
    )
    dp.register_callback_query_handler(
        confirm_delete_user_callback, chat_type=ChatType.PRIVATE,
        state=DeleteUserState.confirm
    )
