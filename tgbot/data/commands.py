from enum import Enum


class Commands(Enum):
    start = 'Стартануть бота'
    features = 'Фичи бота'
    fdetail = 'Подробная информация о каждой фиче'
    howto = 'Как привязать бота к чату'
    add = 'Добавить группу к моим группам'
    reboot = 'Сброс бота'


class ChatAdminCommands(Enum):
    ban = 'Бан пользователя(работает только в группах)'
    unban = 'Разбанить пользователя(работает только в группах)'
    ro = 'Мютить пользователя(работает только в группах)'
    unro = 'Размютить пользователя(работает только в группах)'
    chat = 'Узнать ID чата(работает только в группах)'


class ButtonCommands(Enum):
    update_tariff = 'Изменить тариф 📄'
    tariff_list = 'Посмотреть тариф 📜'
    add_to_chat = 'Добавить бота в чат 🔗'
    users_list = 'Список пользователей 👤'
    delete_users = 'Удалить пользователя 💀'
    my_groups = 'Мои группы 💬'
    buy_subscribe = 'Продлить подписку ⭐'
    bot_settings = 'Настройки бота ⚙️'
    help_commands = 'Помощь по командам 📱'
    bot_features = 'Список фич бота 🤖'
    howto_setup = 'Как привязать бота к чату ❓'
    features_detail = 'Подробная информация о каждой фиче 🦾'
    back = 'Назад 🔙'
    howto_log_chat = 'Как привязать лог чат 📧'
