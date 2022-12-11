from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
TOKEN = open(".token", "r").read()
# TOKEN = 'you_token'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

