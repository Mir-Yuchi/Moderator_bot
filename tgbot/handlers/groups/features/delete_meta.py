from aiogram import Dispatcher
from aiogram.types import Message, ChatType, ContentType


async def delete_meta_info(message: Message):
    await message.delete()


def register_meta_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_meta_info, subscribe_active=True,
        meta_delete_active=True,
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
        content_types=[
            ContentType.LEFT_CHAT_MEMBER,
            ContentType.NEW_CHAT_MEMBERS,
            ContentType.NEW_CHAT_PHOTO,
            ContentType.NEW_CHAT_TITLE,
            ContentType.DELETE_CHAT_PHOTO,
        ]
    )
