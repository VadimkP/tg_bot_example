from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
TOKEN = open(".token", "r").read()
# TOKEN = '5918918851:AAGGPgVdwA64WhPxNOrKI4HJp9vPhQfPE0g'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

