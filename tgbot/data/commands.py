from enum import Enum


class Commands(Enum):
    start = 'Стартануть бота'
    features = 'Фичи бота'
    fdetail = 'Подробная информация о каждой фиче'
    howto = 'Как привязать бота к чату'
    add = 'Добавить группу к моим группам'
    reboot = 'Сброс бота'


class ButtonCommands(Enum):
    add_tariff = 'Добавить тариф 💲'
    del_tariff = 'Удалить тариф 🗑️'
    update_tariff = 'Изменить тариф 📄'
    tariff_list = 'Список тарифов 📜'
    add_to_chat = 'Добавить бота в чат 🔗'
