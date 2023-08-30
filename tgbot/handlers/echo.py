from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hcode

from tgbot.data.commands import Commands


async def bot_echo(message: types.Message):
    text = [
        "Эхо без состояния.",
        "Сообщение:",
        message.text
    ]
    await message.answer('\n'.join(text))


async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Эхо в состоянии {hcode(state_name)}',
        'Содержание сообщения:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text))


async def reboot_bot(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        'Перезапустил бота, нажмите заново на /start',
        reply_markup=ReplyKeyboardRemove()
    )


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*",
                                content_types=types.ContentTypes.ANY)
