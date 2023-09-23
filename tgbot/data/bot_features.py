from enum import Enum

from tgbot.interfaces.features import BotFeatureInfo, FeatureSettings
from tgbot.interfaces.features.antiflood import (
    AntiFloodSettings,
    WorkModeChoice
)
from tgbot.interfaces.features.filter_words import FilterWordsSettings
from tgbot.interfaces.features.log_chat import LogChatSettings


class AntiFlood(Enum):
    info = BotFeatureInfo(
        'Антиспам(Антифлуд) 💬',
        'Антиспам автоматически блокирует массовую отправку одинаковых '
        'сообщений в чате(можно включить/отключить)\nDefault: Выключено'
    )
    settings = AntiFloodSettings(
        False, WorkModeChoice.strict
    )


class MetaInfoDelete(Enum):
    info = BotFeatureInfo(
        'Очистка метаинформаций 🗑️',
        'Очистка метаинформаций с чата(приход/уход/фото группы)\n'
        'Можно включить/выключить\nDefault: Включено'
    )
    settings = FeatureSettings(
        True
    )


class SilenceMode(Enum):
    info = BotFeatureInfo(
        'Тихий режим 🤫',
        'Функция отключения служебных сообщений бота в группе о его действиях'
        '\nDefault: Включено'
    )
    settings = FeatureSettings(
        True
    )


class ObsceneDelete(Enum):
    info = BotFeatureInfo(
        'Антимат ♻️',
        'Очистка нецензурной лексики(маты)'
        '\nDefault: Включено'
    )
    settings = FeatureSettings(
        True
    )


class FilterWords(Enum):
    info = BotFeatureInfo(
        'Фильтрация по словам ♼',
        'Ник пользователей фильтруется по стоп словам которых вы вводите'
        '\nDefault: Выключено'
    )
    settings = FilterWordsSettings(
        False, []
    )


class FilterMedia(Enum):
    info = BotFeatureInfo(
        'Фильтрация по картинкам 🖼️',
        'Удаление картинок с незензурными/запрещенными словами'
        '\nDefault: Включено'
    )
    settings = FeatureSettings(
        True
    )


class LogChat(Enum):
    info = BotFeatureInfo(
        'Лог чат 🗨️',
        'Вся информация о банах/блокировках отображаются там.\n'
        'Также там можно будет разблокировать/блокировать пользователей\n'
        'Default: Выключено'
    )
    settings = LogChatSettings(
        False
    )


class FeaturesList(Enum):
    anti_flood = AntiFlood
    meta_info_delete = MetaInfoDelete
    silence_mode = SilenceMode
    obscene_delete = ObsceneDelete
    filter_words = FilterWords
    filter_media = FilterMedia
    log_chat = LogChat
