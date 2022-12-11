from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_honey = KeyboardButton('🍯 Mёд')
button_honeycomb = KeyboardButton('🔸 Медовые соты')
button_tea = KeyboardButton('🍵 Травяной чай')
button_tableware = KeyboardButton('🍽 Посуда из дерева')
button_other = KeyboardButton('🤭 Кое-что еще')

button_case_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_honey)\
    .add(button_honeycomb).insert(button_tea).insert(button_tableware).insert(button_other)

