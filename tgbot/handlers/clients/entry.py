from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, ChatType, CallbackQuery
)

from tgbot.config import Config
from tgbot.data.commands import Commands, ButtonCommands
from tgbot.keyboards.inline import make_groups_inline_kb
from tgbot.keyboards.reply import (
    USER_START_COMMANDS, USER_GROUP_COMMANDS,
    ADMIN_GROUP_COMMANDS
)
from tgbot.misc.states import GroupsMenuState
from tgbot.models.admin import AdminGroupBot
from tgbot.models.client import BotClient, ClientSubscribe
from tgbot.utils.db import AsyncDbManager
from tgbot.utils.text import load_bot_feature_names, bot_feature_detail_info


async def user_start(message: Message):
    config: Config = message.bot['config']
    if message.from_user.id not in config.tg_bot.admin_ids:
        async with AsyncDbManager().db_session() as session:
            client = await BotClient.get_one(
                session, {'tg_id': message.from_user.id}
            )
            if not client:
                await BotClient.create(
                    session,
                    {
                        'tg_id': message.from_user.id,
                        'username': message.from_user.username,
                        'full_name': message.from_user.full_name
                    }
                )
    txt = (
            'Привет! Это бот-антиспам для вашей группы🛡️\n'
            'Чтобы меня использовать купите подписку(или воспользуйтесь '
            'бесплатным), чтобы узнать подробнее об установке бота на ваш чат '
            'наберите команду /' + Commands.howto.name +
            '\nЧтобы подробнее узнать о моих возможностях наберите команду /'
            + Commands.features.name + '\nВ любой непонятной ситуации' +
            'наберите команду /' + Commands.reboot.name
    )
    await message.reply(txt, reply_markup=USER_START_COMMANDS)


async def features(message: Message):
    inner = (
            '\n\nЧтобы подробно узнать о каждой возможности бота, '
            'набери команду /' + Commands.fdetail.name
    )
    await message.answer('Фичи этого бота 💣💣💣\n\n' + '\n'.join(
        load_bot_feature_names()
    ) + inner)


async def features_detail(message: Message):
    await message.answer('Описание каждой фичи 💣💣\n\n' + '\n\n'.join(
        bot_feature_detail_info()
    ))


async def howto_setup(message: Message):
    txt = (
        'Как установить бота на вашу группу❓\n',
        '1. Купите подписку',
        '2. Добавьте меня в группу и сделайте админом('
        'дайте все права кроме анонимности)',
        '3. Наберите в чате команду /' + Commands.add.name,
        '4. И всё! После этого чат будет отображаться в ваших чатах, и можете '
        'наслаждаться чистым чатом 😇',
        '<strong>❗❗❗ВНИМАНИЕ❗❗❗\nЧтобы бот работал корректно, в чатах не '
        'используйте функцию анонимности администратора</>',
        '<strong>Чтобы посмотреть список ваших групп в боте нажмите '
        'на кнопку Мои группы</>'
    )
    await message.answer('\n'.join(txt))


async def user_chats(message: Message):
    config: Config = message.bot['config']
    admin_user = message.from_user.id in config.tg_bot.admin_ids
    async with AsyncDbManager().db_session() as session:
        if admin_user:
            groups: list[AdminGroupBot] = await AdminGroupBot.get_all(
                session, {'admin_id': message.from_user.id}
            )
        else:
            groups: list[ClientSubscribe] = await ClientSubscribe.get_all(
                session, {'client_id': message.from_user.id}
            )
    if not groups:
        await message.answer('У вас нет подключенных групп')
        return
    await GroupsMenuState.choose_group.set()
    keyboard = await make_groups_inline_kb(message.bot, groups)
    await message.answer('Выберите подходящий чат', reply_markup=keyboard)


async def user_chats_callback(callback: CallbackQuery, state: FSMContext):
    group_id = int(callback.data)
    config: Config = callback.bot['config']
    admin_user = callback.from_user.id in config.tg_bot.admin_ids
    if admin_user:
        keyboard = ADMIN_GROUP_COMMANDS
    else:
        keyboard = USER_GROUP_COMMANDS
    await state.update_data(choose_group=group_id)
    await GroupsMenuState.group_actions.set()
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await callback.bot.send_message(
        callback.from_user.id,
        'Выберите действие',
        reply_markup=keyboard
    )


def register_entry_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_start, commands=[Commands.start.name], state='*',
        commands_prefix='!/', chat_type=ChatType.PRIVATE
    )
    dp.register_message_handler(
        features, commands=[Commands.features.name], state='*',
        commands_prefix='!/',
    )
    dp.register_message_handler(
        features, text=ButtonCommands.bot_features.value,
        chat_type=ChatType.PRIVATE
    )
    dp.register_message_handler(
        howto_setup, commands=[Commands.howto.name], state='*',
        commands_prefix='!/',
    )
    dp.register_message_handler(
        howto_setup, text=ButtonCommands.howto_setup.value,
        chat_type=ChatType.PRIVATE
    )
    dp.register_message_handler(
        features_detail, commands=[Commands.fdetail.name], state='*',
        commands_prefix='!/',
    )
    dp.register_message_handler(
        features_detail, text=ButtonCommands.features_detail.value,
        chat_type=ChatType.PRIVATE
    )
    dp.register_message_handler(
        user_chats, state='*', text=ButtonCommands.my_groups.value,
        chat_type=ChatType.PRIVATE
    )
    dp.register_callback_query_handler(
        user_chats_callback, state=GroupsMenuState.choose_group,
        chat_type=ChatType.PRIVATE
    )
