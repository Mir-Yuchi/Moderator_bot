from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType

from tgbot.data.commands import ButtonCommands
from tgbot.keyboards.inline import yes_or_no
from tgbot.misc.states import AddTariffState
from tgbot.models.tariffs import Tariff
from tgbot.utils.db import AsyncDbManager
from tgbot.utils.text import confirm_create_tariff


async def add_tariff_command(message: Message):
    await AddTariffState.name.set()
    await message.answer(
        'Отлично! Введите название тарифа(она должна быть уникальной'
    )


async def tariff_free_status(message: Message, state: FSMContext):
    async with AsyncDbManager().db_session() as session:
        tariff: Tariff | None = await Tariff.get_one(
            session, {'name': message.text}
        )
    if tariff:
        await message.answer(
            'Тариф с таким названием уже существует\n'
            'Попробуйте ещё раз'
        )
        return
    await state.update_data(name=message.text)
    await AddTariffState.free.set()
    await message.answer('Тариф будет бесплатным??', reply_markup=yes_or_no())


async def tariff_free_status_callback(
    callback: CallbackQuery, state: FSMContext
):
    match callback.data:
        case 'yes':
            await state.update_data(sum=0)
            await AddTariffState.limitation_days.set()
            await callback.bot.send_message(
                callback.from_user.id,
                'Отлично! Теперь введите кол-во дней действия тарифа'
            )
        case _:
            await AddTariffState.sum.set()
            await callback.bot.send_message(
                callback.from_user.id,
                'Введите сумму тарифа(валюта в \u20BD)'
            )
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )


async def add_tariff_sum(message: Message, state: FSMContext):
    if not message.text.isdecimal():
        await message.answer('Вы ввели не число! Попроубуйте ещё раз')
        return
    await state.update_data(sum=int(message.text))
    await AddTariffState.limitation_days.set()
    await message.answer(
        'Отлично! Теперь введите кол-во дней действия тарифа'
    )


async def add_tariff_days(message: Message, state: FSMContext):
    if not message.text.isdecimal():
        await message.answer('Вы ввели не число! Попроубуйте ещё раз')
        return
    await state.update_data(limitation_days=int(message.text))
    await AddTariffState.groups_count.set()
    await message.answer('Введите кол-во групп доступных в рамках тарифа')


async def add_tariff_groups_count(message: Message, state: FSMContext):
    if not message.text.isdecimal():
        await message.answer('Вы ввели не число! Попроубуйте ещё раз')
        return
    await state.update_data(groups_count=int(message.text))
    await AddTariffState.confirm.set()
    async with state.proxy() as data:
        name = data['name']
        limitation_days = data['limitation_days']
        groups_count = data['groups_count']
        tariff_sum = data['sum']
    await message.answer(
        confirm_create_tariff(
            name, limitation_days, groups_count, tariff_sum,
            ('Подтвердите данные и нажмите Да или нет',)
        ),
        reply_markup=yes_or_no()
    )


async def confirm_create_callback(
    callback: CallbackQuery, state: FSMContext
):
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    match callback.data:
        case 'yes':
            async with state.proxy() as data:
                data.pop('free', 0)
                async with AsyncDbManager().db_session() as session:
                    await Tariff.create(session, data)
            await callback.bot.send_message(
                callback.from_user.id,
                'Успешно создал тариф!'
            )
        case _:
            await callback.bot.send_message(
                callback.from_user.id,
                'Отменено ❌'
            )
    await state.finish()


def register_tariff_create_handlers(dp: Dispatcher):
    dp.register_message_handler(
        add_tariff_command, text=ButtonCommands.add_tariff.value,
        chat_type=ChatType.PRIVATE, is_superuser=True,
    )
    dp.register_message_handler(
        tariff_free_status, chat_type=ChatType.PRIVATE, is_superuser=True,
        state=AddTariffState.name
    )
    dp.register_callback_query_handler(
        tariff_free_status_callback, chat_type=ChatType.PRIVATE,
        state=AddTariffState.free
    )
    dp.register_message_handler(
        add_tariff_days, chat_type=ChatType.PRIVATE, is_superuser=True,
        state=AddTariffState.limitation_days
    )
    dp.register_message_handler(
        add_tariff_groups_count, chat_type=ChatType.PRIVATE, is_superuser=True,
        state=AddTariffState.groups_count
    )
    dp.register_message_handler(
        add_tariff_sum, chat_type=ChatType.PRIVATE, is_superuser=True,
        state=AddTariffState.sum
    )
    dp.register_callback_query_handler(
        confirm_create_callback, chat_type=ChatType.PRIVATE,
        state=AddTariffState.confirm
    )
