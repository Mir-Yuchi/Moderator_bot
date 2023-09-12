from aiogram.types import Message


def only_chat_users_handler(func):
    async def wrapper(obj: Message, **kwargs):
        chat_admins = await obj.chat.get_administrators()
        params = {}
        for key, kwarg in kwargs.items():
            if kwarg in func.__annotations__.keys():
                params[key] = kwarg
        for admin in chat_admins:
            if admin.user.id == obj.from_user.id:
                return
        await func(obj, **params)
    return wrapper
