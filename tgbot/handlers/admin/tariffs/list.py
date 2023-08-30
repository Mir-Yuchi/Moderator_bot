from aiogram import Dispatcher
from aiogram.types import Message, ChatType

from tgbot.data.commands import ButtonCommands
from tgbot.models.tariffs import Tariff
from tgbot.utils.db import AsyncDbManager
from tgbot.utils.text import confirm_create_tariff


async def get_all_tariffs(message: Message):
    async with AsyncDbManager().db_session() as session:
        tariffs = await Tariff.get_all(session)
    if not tariffs:
        await message.answer('Тарифов нет')
        return
    response = '<strong>Список тарифов</strong>\n\n'
    for tariff in tariffs:
        beauty_txt = confirm_create_tariff(
            tariff.name, tariff.limitation_days, tariff.groups_count,
            tariff.sum, (f'<strong>📥 {tariff.name} 📥</>',)
        )
        response += beauty_txt + '\n\n'
    await message.answer(response)


def register_tariff_list_handlers(dp: Dispatcher):
    dp.register_message_handler(
        get_all_tariffs, text=ButtonCommands.tariff_list.value,
        chat_type=ChatType.PRIVATE, is_superuser=True,
    )
