from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove, ChatType

from tgbot.data.commands import Commands
from tgbot.utils.text import load_bot_feature_names, bot_feature_detail_info


async def user_start(message: Message):
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
            '\n\nЧтобы узнать о возможностях бота, набери команду /'
            + Commands.fdetail.name
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
        '1. Купите подписку(или используйте бесплатную)',
        '2. Привяжите меня к группе в настройках(нажмите кнопку '
        'добавить группу в меню)',
        '3. Сделайте меня админом(дайте все права кроме анонимности)',
        '4. Если чат не отображается после нажатия на кнопку мои группы '
        'попробуйте в том чате набрать команду /' + Commands.add.value,
        '5. И всё! После этого чат будет отображаться в ваших чатах, и можете '
        'наслаждаться чистым чатом 😇'
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
