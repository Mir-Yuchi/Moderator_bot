from aiogram.types import BotCommand

from tgbot.data.commands import Commands


def load_bot_commands() -> list[BotCommand]:
    return [
        BotCommand(command_obj.name, command_obj.value)
        for command_obj in Commands.__members__.values()
    ]
