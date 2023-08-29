from aiogram import Dispatcher
from aiogram.types import Message, ChatType

from tgbot.data.commands import Commands


async def admin_start(message: Message):
    txt = (
        '👋 Приветствую, админ!',
        'Чтобы узнать о возможностях бота, набери команду /' +
        Commands.features.name
    )
    await message.answer('\n'.join(txt))


def register_admin_entry_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, commands=[Commands.start.name],
        chat_type=ChatType.PRIVATE, is_superuser=True,
    )
