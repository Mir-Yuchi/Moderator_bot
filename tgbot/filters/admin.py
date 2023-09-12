import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from tgbot.config import Config


class AdminFilter(BoundFilter):
    key = 'is_superuser'

    def __init__(self, is_superuser: typing.Optional[bool] = None):
        self.is_superuser = is_superuser

    async def check(self, obj):
        if self.is_superuser is None:
            return False
        config: Config = obj.bot.get('config')
        return (
            obj.from_user.id in config.tg_bot.admin_ids
        ) == self.is_superuser


class ChatAdminFilter(BoundFilter):
    key = 'chat_admin'

    def __init__(self, chat_admin: typing.Optional[bool] = None):
        self.chat_admin = chat_admin

    async def check(self, message: Message):
        if self.chat_admin is None:
            return False
        chat_admins = await message.chat.get_administrators()
        return message.from_user.id in map(
            lambda obj: obj.user.id,
            chat_admins
        )
