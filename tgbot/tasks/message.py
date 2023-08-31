import asyncio

from aiogram import Bot


async def delete_message_after_time(bot: Bot, chat_id: int,
                                    msg_id: int, seconds: int):
    await asyncio.sleep(seconds)
    await bot.delete_message(chat_id, msg_id)
