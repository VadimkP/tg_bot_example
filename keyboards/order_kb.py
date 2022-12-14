from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_order = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('☎️ Отправить контакт', request_contact=True))

