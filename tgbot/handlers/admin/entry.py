from aiogram import Dispatcher
from aiogram.types import Message, ChatType

from tgbot.data.commands import Commands
from tgbot.handlers.echo import reboot_bot
from tgbot.keyboards.reply import SUPERUSER_START_COMMANDS


async def admin_start(message: Message):
    txt = (
        '👋 Приветствую, админ!',
        'Чтобы узнать о возможностях бота, набери команду /' +
        Commands.features.name,
        'В любой непонятной ситуации наберите команду /' + Commands.reboot.name
    )
    await message.answer('\n'.join(txt), reply_markup=SUPERUSER_START_COMMANDS)


def register_admin_entry_handlers(dp: Dispatcher):
    dp.register_message_handler(
        reboot_bot, commands=[Commands.reboot.name],
        state="*", chat_type=ChatType.PRIVATE
    )
    dp.register_message_handler(
        admin_start, commands=[Commands.start.name],
        chat_type=ChatType.PRIVATE, is_superuser=True,
    )
