from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType, CallbackQuery

from tgbot.data.commands import ButtonCommands
from tgbot.data.db_field_names import TARIFF_FIELD_NAMES
from tgbot.keyboards.inline import (
    make_tariff_inline_kb,
    make_inline_kb_from_dict, yes_or_no
)
from tgbot.misc.states import ChangeTariffState
from tgbot.models.tariffs import Tariff
from tgbot.utils.db import AsyncDbManager
from tgbot.utils.text import confirm_create_tariff


async def update_tariff_command(message: Message):
    async with AsyncDbManager().db_session() as session:
        tariffs: list[Tariff] = await Tariff.get_all(session)
    keyboard = make_tariff_inline_kb(tariffs)
    await ChangeTariffState.tariff.set()
    await message.answer('Выберите тариф для изменения', reply_markup=keyboard)


async def update_tariff_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(tariff=int(callback.data))
    await ChangeTariffState.tariff_field.set()
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await callback.bot.send_message(
        callback.from_user.id,
        'Выберите что изменить',
        reply_markup=make_inline_kb_from_dict(TARIFF_FIELD_NAMES, True)
    )


async def update_tariff_field_callback(
    callback: CallbackQuery, state: FSMContext
):
    await state.update_data(tariff_field=callback.data)
    await ChangeTariffState.field_value.set()
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await callback.bot.send_message(
        callback.from_user.id,
        'Введите ' + TARIFF_FIELD_NAMES[callback.data] + ' тарифа'
    )


async def confirm_update_tariff(message: Message, state: FSMContext):
    value = int(message.text) if message.text.isdecimal() else message.text
    await state.update_data(field_value=value)
    await ChangeTariffState.confirm.set()
    async with state.proxy() as data:
        field = TARIFF_FIELD_NAMES[data['tariff_field']]
    await message.answer(
        'Хотите применить изменения?\nИзменения:\n'
        + field + ': ' + value.__str__(),
        reply_markup=yes_or_no()
    )


async def confirm_update_callback(callback: CallbackQuery, state: FSMContext):
    match callback.data:
        case 'yes':
            async with state.proxy() as data:
                id_ = data.get('tariff')
                tariff_field = data.get('tariff_field')
                field_value = data.get('field_value')
            async with AsyncDbManager().db_session() as session:
                tariff = await Tariff.update(
                    session, {'id': id_}, {tariff_field: field_value}
                )
            await callback.bot.send_message(
                callback.from_user.id,
                'Успешно обновил тариф\n\n' + (
                    confirm_create_tariff(
                        tariff.name, tariff.limitation_days,
                        tariff.groups_count, tariff.sum,
                        ('<strong>Обновленные данные</strong>\n',)
                    )
                ) if tariff else '!'
            )
        case _:
            await callback.bot.send_message(
                callback.from_user.id,
                'Отменено ❌'
            )
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await state.finish()


def register_tariff_update_handlers(dp: Dispatcher):
    dp.register_message_handler(
        update_tariff_command, chat_type=ChatType.PRIVATE,
        text=ButtonCommands.update_tariff.value, is_superuser=True
    )
    dp.register_callback_query_handler(
        update_tariff_callback, chat_type=ChatType.PRIVATE,
        state=ChangeTariffState.tariff
    )
    dp.register_callback_query_handler(
        update_tariff_field_callback, chat_type=ChatType.PRIVATE,
        state=ChangeTariffState.tariff_field
    )
    dp.register_message_handler(
        confirm_update_tariff, chat_type=ChatType.PRIVATE,
        state=ChangeTariffState.field_value, is_superuser=True
    )
    dp.register_callback_query_handler(
        confirm_update_callback, chat_type=ChatType.PRIVATE,
        state=ChangeTariffState.confirm,
    )
