from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_load = KeyboardButton('/Добавить')
button_delete = KeyboardButton('/Удалить')
button_stats = KeyboardButton('/Статистика')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete).add(button_stats)
