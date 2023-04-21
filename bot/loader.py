# Файл загрузчика бота и диспетчера

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config.bot import BOT_TOKEN_API


bot = Bot(token=BOT_TOKEN_API)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
