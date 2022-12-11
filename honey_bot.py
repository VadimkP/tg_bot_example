from aiogram.utils import executor
from create_bot import dp
from handlers import navigation
from handlers import admin_mode
from db import sqlite_db


async def on_startup(_):
    print('Bot startup!')
    sqlite_db.sql_start()


navigation.registration_handlers_navigation(dp)
admin_mode.registration_handlers_admin_mode(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
