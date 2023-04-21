# Главный файл - запуска бота

from bot.handlers import *

from aiogram import executor
from bot.loader import dp


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)

