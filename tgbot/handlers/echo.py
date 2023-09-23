from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, ChatType, Message, ContentTypes

from tgbot.data.commands import Commands, ChatAdminCommands, ButtonCommands
from tgbot.utils.text import commands_txt_info


async def bot_echo_all(message: Message):
    text = [
        "Что-то пошло не так...",
        "Наберите команду /" + Commands.reboot.name,
    ]
    await message.answer('\n'.join(text))


async def reboot_bot(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(
        'Перезапустил бота, нажмите заново на /start',
        reply_markup=ReplyKeyboardRemove()
    )


async def bot_commands_help(message: Message):
    client_commands = commands_txt_info(Commands)
    chat_admin_commands = commands_txt_info(ChatAdminCommands)
    txt = (
        '<strong>Команды в личных сообшениях</strong>\n' +
        '\n'.join(client_commands),
        '<strong>Команды в чатах для админов и прочее</strong>\n' +
        '\n'.join(chat_admin_commands),
    )
    await message.answer(
        '\n\n'.join(txt)
    )


async def howto_log_chat(message: Message):
    await message.answer(
        '<b>Как привязать лог чат ❓</b>\n'
        'В чате где админит этот бот наберите команду /' +
        ChatAdminCommands.chat.name + ' чтобы узнать ID чата, дальше в ' +
        'настройках привяжите этот ID к чату\n'
        '<b>❗❗❗ ВНИМАНИЕ ❗❗❗</b>\n1.Бот в лог чате должен быть админом\n'
        '2.В лог чате те кто принимают решение тоже должны быть админами\n'
        '3.Чат который админит этот бот должен быть супергруппой'
    )


def register_echo(dp: Dispatcher):
    dp.register_message_handler(
        bot_commands_help, chat_type=ChatType.PRIVATE,
        text=ButtonCommands.help_commands.value
    )
    dp.register_message_handler(
        howto_log_chat, chat_type=ChatType.PRIVATE,
        text=ButtonCommands.howto_log_chat.value
    )
    dp.register_message_handler(bot_echo_all, state="*",
                                content_types=ContentTypes.ANY,
                                chat_type=ChatType.PRIVATE)
