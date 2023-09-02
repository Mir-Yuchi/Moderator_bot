from aiogram import Dispatcher
from aiogram.types import (
    Message, ChatType, ReplyKeyboardRemove
)

from tgbot.config import Config
from tgbot.data.commands import Commands
from tgbot.models.client import BotClient
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
    await message.reply(txt, reply_markup=ReplyKeyboardRemove())


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


def register_entry_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_start, commands=[Commands.start.name], state='*',
        commands_prefix='!/', chat_type=ChatType.PRIVATE
    )
    dp.register_message_handler(
        features, commands=[Commands.features.name], state='*',
        commands_prefix='!/', chat_type=ChatType.PRIVATE
    )
    dp.register_message_handler(
        howto_setup, commands=[Commands.howto.name], state='*',
        commands_prefix='!/', chat_type=ChatType.PRIVATE
    )
    dp.register_message_handler(
        features_detail, commands=[Commands.fdetail.name], state='*',
        commands_prefix='!/', chat_type=ChatType.PRIVATE
    )
