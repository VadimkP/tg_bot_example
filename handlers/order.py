from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, ContentTypes
from create_bot import dp, bot
from db import sqlite_db
from keyboards import order_kb, navigation_kb


class FSMOrder(StatesGroup):
    number = State()
    name = State()
    location = State()


async def order_run(chat_id):
    await FSMOrder.number.set()
    await bot.send_message(chat_id, "Пришлите нам свой номер телефона",
                           reply_markup=order_kb.button_order)


async def user_number(message: types.Message, state: FSMContext):
    async with state.proxy() as user:
        user['number'] = message.contact.phone_number
    await FSMOrder.next()
    await message.reply('Укажите ваше Имя', reply_markup=ReplyKeyboardRemove())


async def user_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMOrder.next()
    await message.reply("Пришлите адрес доставки\n(Город/Населенный пункт, улица, дом/корпус/строение")


async def user_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.text

    cart = await sqlite_db.sql_read_cart(message.from_user.id)
    i = 0
    dc = {}
    for ct in cart:
        i += 1
        dc[i] = ct[0]
    user_data = await state.get_data()
    await bot.send_message(-1001680885060, f"<b>Новый заказ!</b>"
                                           f"\n\nИмя: {user_data['name']}"
                                           f"\nТелефон: {user_data['number']}"
                                           f"\nАдрес: {user_data['location']}"
                                           f"\n\n<b>Заказ:</b>"
                                           f"{dc}\n",
                           parse_mode="HTML")
    await message.reply("Заказ передан.\nСпасибо что выбрали нас 😉",
                        reply_markup=navigation_kb.button_case_menu)

    await state.finish()
    await sqlite_db.sql_del_all_user_cart(message.from_user.id)


def registration_handlers_order(dp: Dispatcher):
    dp.register_message_handler(order_run, state=None)
    dp.register_message_handler(user_number, content_types=ContentTypes.CONTACT,
                                state=FSMOrder.number)
    dp.register_message_handler(user_name, state=FSMOrder.name)
    dp.register_message_handler(user_location, state=FSMOrder.location)

