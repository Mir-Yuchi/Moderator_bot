from enum import Enum


class Commands(Enum):
    start = 'Стартануть бота'
    features = 'Фичи бота'
    fdetail = 'Подробная информация о каждой фиче'
    howto = 'Как привязать бота к чату'
    add = 'Добавить группу к моим группам'
    reboot = 'Сброс бота'


class ButtonCommands(Enum):
    update_tariff = 'Изменить тариф 📄'
    tariff_list = 'Посмотреть тариф 📜'
    add_to_chat = 'Добавить бота в чат 🔗'
    users_list = 'Список пользователей 👤'
    delete_users = 'Удалить пользователя 💀'
    my_groups = 'Мои группы 💬'
    buy_subscribe = 'Продлить подписку ⭐'
    bot_settings = 'Настройки бота ⚙️'
