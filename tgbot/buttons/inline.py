from aiogram.types import InlineKeyboardButton

YES = InlineKeyboardButton('Да ✅', callback_data='yes')
NO = InlineKeyboardButton('Нет ❌', callback_data='no')
CANCEL = InlineKeyboardButton('Главное меню', callback_data='cancel')
BACK = InlineKeyboardButton('🔙 Назад', callback_data='back')
