from aiogram.dispatcher.filters.state import StatesGroup, State


class AddTariffState(StatesGroup):
    name = State()
    free = State()
    sum = State()
    limitation_days = State()
    groups_count = State()
    confirm = State()


class DeleteTariffState(StatesGroup):
    callback = State()
    confirm = State()


class ChangeTariffState(StatesGroup):
    tariff = State()
    tariff_field = State()
    field_value = State()
    confirm = State()
