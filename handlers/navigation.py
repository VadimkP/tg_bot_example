from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot, dp
from db import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import navigation_kb

urlContacts = InlineKeyboardMarkup(row_width=1)
urlInsta = InlineKeyboardButton(text='Инстаграм', url='https://www.instagram.com/altay_honey__/')
urlTg = InlineKeyboardButton(text='Телеграм Канал', url='https://t.me/altay_honey')
urlContacts.add(urlInsta, urlTg)


async def help_handler(message: types.Message):
    try:
        await sqlite_db.order(message.from_user.id, message.from_user.full_name)
    except:
        print(f'Пользователь {message.from_user.full_name} уже есть в таблице users!')
    await bot.send_message(message.from_user.id, 'Добро пожаловать 🌻\n\n'
                                                 '— у нас вы сможете насладиться тонким вкусом и натуральной текстурой '
                                                 'настоящего мёда с алтайских полей под чашечку травяного чая 🍃'
                                                  )


async def menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери из меню, что вам по душе 😉',
                           reply_markup=navigation_kb.button_case_menu)


async def submenu_honey(message: types.Message):
    honey = await sqlite_db.sql_read_honey()
    for hon in honey:
        await bot.send_photo(message.from_user.id, hon[0], f'{hon[2]}\n {hon[3]}\n\nЦена: {hon[-1]}')


async def submenu_honeycomb(message: types.Message):
    honeycomb = await sqlite_db.sql_read_honeycomb()
    for honc in honeycomb:
        await bot.send_photo(message.from_user.id, honc[0], f'{honc[2]}\n {honc[3]}\n\nЦена: {honc[-1]}')


async def submenu_tea(message: types.Message):
    tea = await sqlite_db.sql_read_tea()
    for t in tea:
        await bot.send_photo(message.from_user.id, t[0], f'{t[2]}\n {t[3]}\n\nЦена: {t[-1]}')


async def submenu_tableware(message: types.Message):
    tablew = await sqlite_db.sql_read_tableware()
    for tw in tablew:
        await bot.send_photo(message.from_user.id, tw[0], f'{tw[2]}\n {tw[3]}\n\nЦена: {tw[-1]}')


async def submenu_other(message: types.Message):
    other = await sqlite_db.sql_read_other()
    for oth in other:
        await bot.send_photo(message.from_user.id, oth[0], f'{oth[2]}\n {oth[3]}\n\nЦена: {oth[-1]}')


async def about_us(message: types.Message):
    await bot.send_message(message.from_user.id, 'Какое-то описание, или можно придумать другую кнопку/функционал')


async def contacts(message: types.Message):
    await message.answer('Наши Контакты:', reply_markup=urlContacts)


def registration_handlers_navigation(dp: Dispatcher):
    dp.register_message_handler(help_handler, commands=['start'])
    dp.register_message_handler(menu, commands=['menu'])
    dp.register_message_handler(submenu_honey, Text(equals="🍯 Mёд", ignore_case=True))
    dp.register_message_handler(submenu_honeycomb, Text(equals="🔸 Медовые соты", ignore_case=True))
    dp.register_message_handler(submenu_tea, Text(equals="🍵 Травяной чай", ignore_case=True))
    dp.register_message_handler(submenu_tableware, Text(equals="🍽 Посуда из дерева", ignore_case=True))
    dp.register_message_handler(submenu_other, Text(equals="🤭 Кое-что еще", ignore_case=True))
    dp.register_message_handler(about_us, commands=['about_us'])
    dp.register_message_handler(contacts, commands=['contacts'])
