from datetime import datetime, timedelta

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update, ChatType
from redis.asyncio import Redis

from tgbot.data.bot_features import FeaturesList
from tgbot.interfaces.features.antiflood import AntiSpamMsg
from tgbot.models.bot import RedisTgBotSettings


class AntiSpamMiddleware(BaseMiddleware):
    messages: dict[int, dict[int, list[AntiSpamMsg]]] = {}
    times: dict[int, dict[int]] = {}

    def __init__(self, msg_seconds_limit: int = 5, msg_count_limit: int = 5):
        self.msg_seconds_limit = msg_seconds_limit
        self.msg_count_limit = msg_count_limit
        super().__init__()

    async def check_time(self, group_id: int, user_id: int):
        now = datetime.utcnow()
        group_check = self.times.get(group_id)
        if not group_check:
            self.times[group_id] = {}
        user_check = self.times[group_id].get(user_id)
        if user_check:
            if (
                now - self.times[group_id][user_id] >
                timedelta(seconds=self.msg_seconds_limit)
            ):
                self.messages[group_id][user_id].clear()
                self.times[group_id][user_id] = now
        else:
            self.times[group_id][user_id] = now

    async def check_messages(self, upd: Update):
        if not upd.message or upd.message.chat.type == ChatType.PRIVATE:
            return
        redis: Redis = upd.bot['redis_db']
        group_id = upd.message.chat.id
        settings = await RedisTgBotSettings(
            group_id
        ).load_settings(redis)
        if not settings:
            return
        antispam = settings[FeaturesList.anti_flood.name]
        if not antispam['on']:
            return
        user_id = upd.message.from_user.id
        admins = await upd.bot.get_chat_administrators(group_id)
        for admin in admins:
            if admin.user.id == user_id:
                return
        group_check = self.messages.get(group_id)
        if not group_check:
            self.messages[group_id] = {}
        user_last_msgs = self.messages[group_id].get(user_id)
        if user_last_msgs is None:
            self.messages[group_id][user_id] = []
        else:
            self.messages[group_id][user_id].append(
                AntiSpamMsg(upd.message.text, upd.message.message_id)
            )
            await self.check_time(group_id, user_id)
            if any([
                len(self.messages[group_id][user_id]) >= self.msg_count_limit,
                len(self.messages[group_id][user_id]) !=
                len({msg.msg_text for msg in self.messages[group_id][user_id]})
            ]):
                await upd.bot.restrict_chat_member(
                    group_id, user_id, None, can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                )
                for msg in self.messages[group_id][user_id]:
                    await upd.bot.delete_message(
                        group_id, msg.msg_id
                    )
                raise CancelHandler()

    async def on_process_update(self, upd: Update, data: dict):
        await self.check_messages(upd)
