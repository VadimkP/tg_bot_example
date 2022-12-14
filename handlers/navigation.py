from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot, dp
from db import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from keyboards import navigation_kb
from handlers import order


urlContacts = InlineKeyboardMarkup(row_width=1)
urlInsta = InlineKeyboardButton(text='Инстаграм', url='https://www.instagram.com/altay_honey__/')
urlTg = InlineKeyboardButton(text='Телеграм Канал', url='https://t.me/altay_honey_spb')
urlContacts.add(urlInsta, urlTg)


async def start_handler(message: types.Message):
    await bot.send_message(message.from_user.id, 'Добро пожаловать 🌻\n\n'
                                                 '— у нас вы сможете насладиться тонким вкусом и натуральной текстурой '
                                                 'настоящего мёда с алтайских полей под чашечку травяного чая 🍃')
    try:
        await sqlite_db.users_stats(message.from_user.id, message.from_user.full_name)
    except:
        print(f'Пользователь {message.from_user.full_name} уже есть в таблице users!')


async def menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите из меню, что вам по душе 😉',
                           reply_markup=navigation_kb.button_case_menu)


async def add_to_cart(callback_query: types.CallbackQuery):
    await sqlite_db.sql_add_cart(callback_query.data.replace('Добавить ', ''), callback_query.message.chat.id)
    await callback_query.answer(text=f'{callback_query.data.replace("Добавить ", "")} добавлено.', show_alert=True)


async def submenu_honey(message: types.Message):
    honey = await sqlite_db.sql_read_honey()
    for hon in honey:
        await bot.send_photo(message.from_user.id, hon[0], f'<b>{hon[2]}</b>\n\n{hon[3]}\n\n<b>Цена:</b>\n{hon[-1]}',
                             parse_mode="HTML", reply_markup=InlineKeyboardMarkup()
                             .add(InlineKeyboardButton(text=f'Добавить в корзину {hon[2]}',
                                                       callback_data=f'Добавить {hon[2]}')))


async def submenu_honeycomb(message: types.Message):
    honeycomb = await sqlite_db.sql_read_honeycomb()
    for honc in honeycomb:
        await bot.send_photo(message.from_user.id, honc[0],
                             f'<b>{honc[2]}</b>\n\n{honc[3]}\n\n<b>Цена:</b>\n{honc[-1]}',
                             parse_mode="HTML", reply_markup=InlineKeyboardMarkup()
                             .add(InlineKeyboardButton(text=f'Добавить в корзину {honc[2]}',
                                                       callback_data=f'Добавить {honc[2]}')))


async def submenu_tea(message: types.Message):
    tea = await sqlite_db.sql_read_tea()
    for t in tea:
        await bot.send_photo(message.from_user.id, t[0], f'<b>{t[2]}</b>\n\n{t[3]}\n\n<b>Цена:</b>\n{t[-1]}',
                             parse_mode="HTML", reply_markup=InlineKeyboardMarkup()
                             .add(InlineKeyboardButton(text=f'Добавить в корзину {t[2]}',
                                                       callback_data=f'Добавить {t[2]}')))


async def submenu_tableware(message: types.Message):
    tablew = await sqlite_db.sql_read_tableware()
    for tw in tablew:
        await bot.send_photo(message.from_user.id, tw[0], f'<b>{tw[2]}</b>\n\n{tw[3]}\n\n<b>Цена:</b>\n{tw[-1]}',
                             parse_mode="HTML", reply_markup=InlineKeyboardMarkup()
                             .add(InlineKeyboardButton(text=f'Добавить в корзину {tw[2]}',
                                                       callback_data=f'Добавить {tw[2]}')))


async def submenu_other(message: types.Message):
    other = await sqlite_db.sql_read_other()
    for oth in other:
        await bot.send_photo(message.from_user.id, oth[0], f'<b>{oth[2]}</b>\n{oth[3]}\n\n<b>Цена:</b>{oth[-1]}',
                             parse_mode="HTML", reply_markup=InlineKeyboardMarkup()
                             .add(InlineKeyboardButton(text=f'Добавить в корзину {oth[2]}',
                                                       callback_data=f'Добавить {oth[2]}')))


async def del_one_pos_from_cart(callback_query: types.CallbackQuery):
    await sqlite_db.sql_del_one_pos_from_cart(callback_query.data.replace('Удалить из корзины ', ''),
                                              callback_query.message.chat.id)
    await callback_query.answer(text=f'{callback_query.data.replace("Удалить из корзины ", "")} удалено.',
                                show_alert=True)


async def del_all_cart(callback_query: types.CallbackQuery):
    await sqlite_db.sql_del_all_user_cart(callback_query.message.chat.id)
    await callback_query.answer(text=f'Корзина очищена', show_alert=True)


async def confirm_order(callback_query: types.CallbackQuery):
    f = await sqlite_db.sql_read_cart(callback_query.message.chat.id)
    if not f:
        await callback_query.answer(text=f'Ваша корзина пуста', show_alert=True)
    else:
        try:
            await order.order_run(callback_query.message.chat.id)
        except:
            await callback_query.answer(text='Что-то пошло не так, попробуйте еще раз.')
        # print(callback_query.message.chat.id)


async def submenu_cart(message: types.Message):
    cart = await sqlite_db.sql_read_cart(message.from_user.id)
    i = 0
    for ct in cart:
        i += 1
        await bot.send_message(message.from_user.id, f'{i}. {ct[0]}\nЦена: {ct[1]}\n\n',
                               reply_markup=InlineKeyboardMarkup().
                               add(InlineKeyboardButton(text=f'Удалить из корзины {ct[0]} ?',
                                                        callback_data=f'Удалить из корзины {ct[0]}')))
    await bot.send_message(message.from_user.id, f'Итого позиций в корзине: {i}\nДля оформления заказа нажмите "Подтвердить заказ".'
                                                 f'\nБот спросит у вас номер телефон, имя и '
                                                 f'адрес для доставки',
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Подтвердить заказ',
                                                                                        callback_data=f'Подтвердить заказ')).
                           add(InlineKeyboardButton(text=f'Очистить корзину',
                                                    callback_data=f'Очистить корзину')))


async def about_us(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет 🌻'
                                                 '\n\nМы – Аня, Максим и Алиса – приехали с Алтая и привезли с собой натуральный мёд. '
                                                 '\n\n<i>Сейчас мы на стадии развития нашего медового бизнеса и оформления'
                                                 'документов о качестве. Это не быстрый процесс, но мы стараемся</i> 🐝'
                                                 '\n\nЕсли Вы уже обращались к нам, то общались со мной, с Аней 👋🏻'
                                                 '– я веду аккаунты в соц.сетях; раскладываю мёд по баночкам, а травы по пакетикам; '
                                                 'принимаю заказы и помогаю Вам определиться с выбором 💛'
                                                 '\nМаксим отвечает за логистическую часть нашего дела: принимает поставки мёда'
                                                 ' и развозит Ваши заказы.'
                                                 '\nА Алиса – наша маленькая дочь, чьё рождение сподвигло к созданию этого'
                                                 ' медового магазина 🍯'
                                                 '\n\n<b>Откуда мы берём мёд?</b>'
                                                 '\nЯ не ответила?'
                                                 '\nМы начинали со скромных объёмов родительской пасеки. А теперь покупаем его '
                                                 'у наших добрых друзей, которые занимаются этим всю свою жизнь'
                                                 '\n💛 Мы гордимся качеством нашего мёда и скоро сможем подтвердить это официально!'
                                                 '\n\n⚠️ Мёд не подвергается термообработке и разбавлению. '
                                                 'В нем нет никаких добавок химии и иных составляющих. 100% натуральный продукт.',
                           parse_mode="HTML")


async def contacts(message: types.Message):
    await message.answer('Наши Контакты:', reply_markup=urlContacts)


def registration_handlers_navigation(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(menu, commands=['menu'])
    dp.register_callback_query_handler(add_to_cart, lambda x: x.data and x.data.startswith('Добавить '))
    dp.register_message_handler(submenu_honey, Text(equals="🍯 Mёд", ignore_case=True))
    dp.register_message_handler(submenu_honeycomb, Text(equals="🔸 Медовые соты", ignore_case=True))
    dp.register_message_handler(submenu_tea, Text(equals="🍵 Травяной чай", ignore_case=True))
    dp.register_message_handler(submenu_tableware, Text(equals="🍽 Посуда из дерева", ignore_case=True))
    dp.register_message_handler(submenu_other, Text(equals="🤭 Кое-что еще", ignore_case=True))
    dp.register_callback_query_handler(del_one_pos_from_cart, lambda x: x.data and x.data.startswith('Удалить из корзины '))
    dp.register_callback_query_handler(del_all_cart, lambda x: x.data and x.data.startswith('Очистить корзину'))
    dp.register_callback_query_handler(confirm_order, lambda x: x.data and x.data.startswith('Подтвердить заказ'))
    dp.register_message_handler(submenu_cart, Text(equals="🛒 Корзина", ignore_case=True))
    dp.register_message_handler(about_us, commands=['about_us'])
    dp.register_message_handler(contacts, commands=['contacts'])

