from aiogram import Dispatcher
from aiogram.types import Message, ChatType

from tgbot.data.commands import ButtonCommands
from tgbot.models.client import BotClient
from tgbot.utils.db import AsyncDbManager
from tgbot.utils.text import numerate_iterable_txt, mention_user_html


async def client_list(message: Message):
    async with AsyncDbManager().db_session() as session:
        clients: list[BotClient] = await BotClient.get_all(session)
    txt = []
    for client in clients:
        txt.append(mention_user_html(client.tg_id, client.full_name))
    await message.answer('Список пользователей 👤\n\n' + '\n'.join(
        numerate_iterable_txt(txt)
    ))


def register_client_list_handlers(dp: Dispatcher):
    dp.register_message_handler(
        client_list, chat_type=ChatType.PRIVATE,
        text=ButtonCommands.users_list.value, is_superuser=True,
    )
