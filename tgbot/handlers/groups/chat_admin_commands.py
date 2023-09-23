from aiogram import Dispatcher
from aiogram.types import Message, ChatType

from tgbot.data.commands import ChatAdminCommands


async def ban(message: Message):
    await message.bot.ban_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id
    )
    await message.reply(
        'Нарушитель забанен'
    )


async def unban(message: Message):
    await message.bot.unban_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        only_if_banned=True
    )
    await message.reply(
        'Пользователь разбанен'
    )


async def ro(message: Message):
    await message.bot.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        None, can_send_messages=False, can_send_media_messages=False,
        can_send_other_messages=False, can_add_web_page_previews=False,
    )
    await message.reply('Пользователь может только читать сообщения')


async def unro(message: Message):
    await message.bot.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        None, can_send_messages=True, can_send_media_messages=True,
        can_send_other_messages=True, can_add_web_page_previews=True,
    )
    await message.reply('Пользователь снова может написать сообщения')


async def chat_id_get(message: Message):
    await message.reply(
        'ID чата: ' + message.chat.id.__str__()
    )


def register_chat_admin_commands(dp: Dispatcher):
    dp.register_message_handler(
        ban, chat_admin=True, commands=[ChatAdminCommands.ban.name],
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]
    )
    dp.register_message_handler(
        unban, chat_admin=True, commands=[ChatAdminCommands.unban.name],
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]
    )
    dp.register_message_handler(
        ro, chat_admin=True, commands=[ChatAdminCommands.ro.name],
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]
    )
    dp.register_message_handler(
        unro, chat_admin=True, commands=[ChatAdminCommands.unro.name],
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]
    )
    dp.register_message_handler(
        chat_id_get, chat_admin=True, commands=[ChatAdminCommands.chat.name],
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]
    )
