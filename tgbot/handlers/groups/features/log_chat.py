from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ChatType


async def log_chat_callback(callback: CallbackQuery):
    action, user_id, chat_id = callback.data.split('__')
    user_id = int(user_id)
    chat_id = int(chat_id)
    match action:
        case 'ro':
            await callback.bot.restrict_chat_member(
                chat_id, user_id, None, can_send_messages=False,
                can_send_other_messages=False, can_send_media_messages=False,
                can_add_web_page_previews=False
            )
            await callback.bot.send_message(
                callback.message.chat.id,
                'Успешно заглушил пользователя'
            )
        case 'unro':
            await callback.bot.restrict_chat_member(
                chat_id, user_id, None, can_send_messages=True,
                can_send_other_messages=True, can_send_media_messages=True,
                can_add_web_page_previews=True
            )
            await callback.bot.send_message(
                callback.message.chat.id,
                'Успешно размютил пользователя'
            )
        case 'unban':
            await callback.bot.unban_chat_member(
                chat_id, user_id, True
            )
            await callback.bot.send_message(
                callback.message.chat.id,
                'Успешно разбанил пользователя'
            )
        case _:
            await callback.bot.ban_chat_member(
                chat_id, user_id
            )
            await callback.bot.send_message(
                callback.message.chat.id,
                'Успешно забанил пользователя'
            )


def register_log_chat_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        log_chat_callback, chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
        chat_admin=True
    )
