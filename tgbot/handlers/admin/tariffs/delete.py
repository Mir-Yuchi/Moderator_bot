from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, ChatType, CallbackQuery
)

from tgbot.data.commands import ButtonCommands
from tgbot.keyboards.inline import yes_or_no, make_tariff_inline_kb
from tgbot.misc.states import DeleteTariffState
from tgbot.models.tariffs import Tariff
from tgbot.utils.db import AsyncDbManager


async def delete_tariff_command(message: Message):
    async with AsyncDbManager().db_session() as session:
        tariffs: list[Tariff] = await Tariff.get_all(session)
    keyboard = make_tariff_inline_kb(tariffs)
    await DeleteTariffState.callback.set()
    await message.answer('Выберите тариф для удаления', reply_markup=keyboard)


async def delete_tariff_callback(callback: CallbackQuery, state: FSMContext):
    field_id = int(callback.data)
    await state.update_data(callback=field_id)
    async with AsyncDbManager().db_session() as session:
        tariff: Tariff = await Tariff.get_one(
            session, {'id': field_id}
        )
    await DeleteTariffState.confirm.set()
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await callback.bot.send_message(
        callback.from_user.id,
        'Вы точно хотите удалить тариф ' + tariff.name + ' ❓',
        reply_markup=yes_or_no()
    )


async def confirm_delete_tariff_callback(
    callback: CallbackQuery, state: FSMContext
):
    match callback.data:
        case 'yes':
            async with AsyncDbManager().db_session() as session:
                async with state.proxy() as data:
                    field_id = data.pop('callback')
                await Tariff.delete(session, {'id': field_id})
            await callback.bot.send_message(
                callback.from_user.id,
                'Успешно удалил тариф'
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


def register_delete_tariff_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_tariff_command, chat_type=ChatType.PRIVATE,
        text=ButtonCommands.del_tariff.value, is_superuser=True
    )
    dp.register_callback_query_handler(
        delete_tariff_callback, chat_type=ChatType.PRIVATE,
        is_superuser=True, state=DeleteTariffState.callback
    )
    dp.register_callback_query_handler(
        confirm_delete_tariff_callback, chat_type=ChatType.PRIVATE,
        is_superuser=True, state=DeleteTariffState.confirm
    )
