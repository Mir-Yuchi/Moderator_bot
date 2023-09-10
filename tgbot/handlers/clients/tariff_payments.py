from datetime import datetime, timedelta

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, ChatType, LabeledPrice,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery,
    PreCheckoutQuery, ContentType
)
from redis.asyncio import Redis

from tgbot.config import Config
from tgbot.data.commands import ButtonCommands
from tgbot.misc.states import GroupsMenuState, SubscribePaymentState
from tgbot.models.bot import RedisTgBotSettings
from tgbot.models.client import ClientSubscribe
from tgbot.models.tariffs import Tariff
from tgbot.services.payments import PaymentsManager
from tgbot.utils.db import AsyncDbManager
from tgbot.utils.features import load_all_feature_settings


async def payment_choose_tariff(message: Message, state: FSMContext):
    async with state.proxy() as data:
        group_id: int = data.get('choose_group')
    await state.finish()
    async with AsyncDbManager().db_session() as session:
        tariff: Tariff | None = await Tariff.get_one(session)
    if not tariff:
        await message.answer('Тариф не существует!')
        return
    keyboard = InlineKeyboardMarkup()
    month_sum, half_year_sum, year_sum = [tariff.sum] + [
        PaymentsManager.calc_price_with_discount(tariff.sum * mul)
        for mul in [6, 12]
    ]
    month_days, half_year_days, year_days = [
        mul * tariff.limitation_days
        for mul in [1, 6, 12]
    ]
    keyboard.add(InlineKeyboardButton(
        f'STANDART({tariff.limitation_days} дней) {month_sum} \u20BD',
        callback_data=f'{month_sum}_{month_days}_{group_id}'
    ))
    keyboard.add(InlineKeyboardButton(
        f'SILVER({half_year_days} дней) {half_year_sum} \u20BD',
        callback_data=f'{half_year_sum}_{half_year_days}_{group_id}'
    ))
    keyboard.add(InlineKeyboardButton(
        f'GOLD({year_days} дней) {year_sum} \u20BD',
        callback_data=f'{year_sum}_{year_days}_{group_id}'
    ))
    await SubscribePaymentState.group_id.set()
    await message.answer('Выберите тариф для подписки', reply_markup=keyboard)


async def payment_subscribe_invoice_callback(callback: CallbackQuery,
                                             state: FSMContext):
    pay_sum, pay_days, group_id = map(int, callback.data.split('_'))
    await SubscribePaymentState.invoice.set()
    async with AsyncDbManager().db_session() as session:
        tariff = await Tariff.get_one(session)
    me = await callback.bot.get_me()
    payment_manager = PaymentsManager(
        callback.from_user.id,
        group_id,
        'Оплата по тарифу',
        'Оплата по тарифу ' + tariff.name + ' в боте ' + me.full_name,
        pay_sum,
        pay_days
    )
    await state.update_data(group_id=group_id,
                            invoice=f'{pay_sum}_{pay_days}')
    config: Config = callback.bot['config']
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await callback.bot.send_invoice(
        callback.from_user.id,
        payment_manager.product_name,
        payment_manager.product_title,
        payment_manager.payload,
        config.tg_bot.SUBSCRIBE_PAYMENT_PROVIDER_TOKEN,
        config.tg_bot.PAYMENTS_CURRENCY,
        [LabeledPrice(payment_manager.product_name, payment_manager.amount)]
    )


async def pre_checkout_callback(checkout_query: PreCheckoutQuery,
                                state: FSMContext):
    async with state.proxy() as data:
        pay_sum, pay_days = map(int, data.get('invoice').split('_'))
    if checkout_query.total_amount // 100 != pay_sum:
        await state.finish()
        await checkout_query.bot.answer_pre_checkout_query(
            checkout_query.id,
            False,
            'Суммы платежа не совпадают\nПопробуйте заново'
        )
        return
    await SubscribePaymentState.finish.set()
    await checkout_query.bot.answer_pre_checkout_query(
        checkout_query.id,
        True,
    )


async def result_payment(message: Message, state: FSMContext):
    async with state.proxy() as data:
        group_id = data['group_id']
        pay_sum, pay_days = map(int, data.get('invoice').split('_'))
    settings = load_all_feature_settings()
    async with AsyncDbManager().db_session() as session:
        subscribe: ClientSubscribe | None = await ClientSubscribe.get_one(
            session, {'client_id': message.from_user.id, 'group_id': group_id}
        )
        tariff: Tariff = await Tariff.get_one(session)
        if subscribe:
            expire_date_next = None
            if subscribe.expired():
                expire_date_next = datetime.utcnow() + timedelta(pay_days)
            else:
                expire_date_next = subscribe.expire_date + timedelta(pay_days)
            subscribe = await ClientSubscribe.update(
                session,
                {'client_id': message.from_user.id, 'group_id': group_id},
                {'expire_date': expire_date_next}
            )
        else:
            subscribe = await ClientSubscribe.create(
                session,
                {
                    'client_id': message.from_user.id,
                    'group_id': group_id,
                    'tariff_id': tariff.id,
                    'expire_date': datetime.utcnow() + timedelta(pay_days),
                    'bot_settings': settings,
                },
            )
    await state.finish()
    redis: Redis = message.bot['redis_db']
    rdb_obj = RedisTgBotSettings(
        group_id, settings
    )
    await rdb_obj.set_settings(redis)
    await message.answer(
        f'Вы успешно продлили подписку! Подписка действует до:'
        f' {subscribe.expire_date.strftime("%d.%m.%Y:%H:%M")}'
    )


def register_payment_handlers(dp: Dispatcher):
    dp.register_message_handler(
        payment_choose_tariff, text=ButtonCommands.buy_subscribe.value,
        state=GroupsMenuState.group_actions, chat_type=ChatType.PRIVATE
    )
    dp.register_callback_query_handler(
        payment_subscribe_invoice_callback,
        state=SubscribePaymentState.group_id, chat_type=ChatType.PRIVATE
    )
    dp.register_pre_checkout_query_handler(
        pre_checkout_callback, state=SubscribePaymentState.invoice,
    )
    dp.register_message_handler(
        result_payment, state=SubscribePaymentState.finish,
        chat_type=ChatType.PRIVATE,
        content_types=[ContentType.SUCCESSFUL_PAYMENT]
    )
