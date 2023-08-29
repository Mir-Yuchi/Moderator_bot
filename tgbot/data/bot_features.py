from enum import Enum

from tgbot.interfaces.features import BotFeatureInfo
import tgbot.interfaces.features.antiflood as af_feat


# FEATURES = [
#     {
#         'name': 'Антиспам',
#         'title': 'Антиспам автоматически блокирует '
#                  'массовую отправку сообщений в чате',
#     },
#     {
#         'name': 'Антимат',
#         'title': 'Бот определяет матерное слово и автоматом удаляет',
#     },
#     {
#         'name': 'Удаление ссылок',
#         'title': 'Удаление ссылок(за исключением разрешённых пользователей)'
#                  ' которые отправил пользователь',
#     },
#     {
#         'name': 'Очистка информации о действий в чате',
#         'title': 'Очистка информации о входе/выходе/кика пользователей',
#     },
#     {
#         'name': 'Капча для новых участников',
#         'title': 'Новые участники должны будут пройти капчу(нажатие кнопки) '
#                  'в течении минуты, иначе будут выгнаны с чата',
#     },
#     {
#         'name': 'Модерация пользователей',
#         'title': 'Админы могут ограничить/кикнуть пользователей из чата',
#     },
#     {
#         'name': 'Очистка группы от удалённых аккаунтов',
#         'title': 'Кик из чата удалённых аккаунтов',
#     },
#     {
#         'name': 'Тихий режим работы',
#         'title': 'Бот обычно комментирует свои действия, если тихий режим '
#                  'включён, он ничего не будет комментировать и работать тихо',
#     },
#     {
#         'name': 'Система уведомлений',
#         'title': 'Отправка сообщений, '
#                  'медиаконтента в ваши чаты из админки',
#     },
#     {
#         'name': 'Удаление сообщений(участников) по ключевым словам',
#         'title': 'Тут всё просто, вы вводите необходимые слова, бот '
#                  'автоматически удаляет сообщения(участников группы тоже '
#                  'можно включить) по этим ключевым словам',
#     },
#     {
#         'name': 'Чёрный список участников',
#         'title': 'Участники которые не могут вступить в чат(определяете вы)',
#     },
#     {
#         'name': 'Белый список участников',
#         'title': 'Участники которые могут публиковать '
#                  'новости/медиаконтент и тп',
#     },
#     {
#         'name': 'Ежедневные отчёты о работе бота',
#         'title': 'Бот ежедневно будет вас уведомить о статистике всего(прихода'
#                  ' пользователей, удаленных сообщений и тп)',
#     },
#     {
#         'name': 'Ночной режим',
#         'title': 'Бот на ночь вырубает любые действия в чате',
#     },
#     {
#         'name': 'Закрыть группу на время',
#         'title': 'Бот закрывает группу на время и кикает всех кто пытается '
#                  'войти',
#     },
#     {
#         'name': 'Управление пересланными сообщениями',
#         'title': 'Бот может оставить/удалить пересланные сообщения',
#     },
#     {
#         'name': 'Управление правилами группы',
#         'title': 'Вы можете добавить/удалить правила группы в боте, в свою '
#                  'очередь бот напоминает о правилах группы пользователей',
#     },
#     {
#         'name': 'Предупреждения(бан) пользоватей модераторами',
#         'title': 'Админы могут давать предупреждения пользователям, и когда '
#                  'число предупреждений достигает определённое кол-во(решается '
#                  'в админке) то принять определённую меру этому пользователю'
#                  '(тоже решается админом)',
#     }
# ]


class AntiFlood(Enum):
    info = BotFeatureInfo(
        1,
        'Антиспам(Антифлуд) 💬',
        'Антиспам автоматически блокирует массовую отправку одинаковых'
        'сообщений в чате'
    )
    settings = af_feat.AntiFloodSettings(
        False, af_feat.WorkModeChoice.strict
    )


class FeaturesList(Enum):
    anti_flood = AntiFlood