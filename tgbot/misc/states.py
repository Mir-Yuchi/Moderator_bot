from aiogram.dispatcher.filters.state import StatesGroup, State


class DeleteUserState(StatesGroup):
    callback = State()
    confirm = State()


class ChangeTariffState(StatesGroup):
    tariff = State()
    tariff_field = State()
    field_value = State()
    confirm = State()


class GroupsMenuState(StatesGroup):
    choose_group = State()
    group_actions = State()


class SubscribePaymentState(StatesGroup):
    group_id = State()
    invoice = State()
    finish = State()


class FeatureSettingsState(StatesGroup):
    group_id = State()
    feature_settings = State()
    set_settings = State()
    add_word_list = State()
    set_log_chat_id = State()
