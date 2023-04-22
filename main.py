# Главный файл - запуска бота


from bot.handlers import *

from aiogram import executor
from bot.loader import dp

from db.database import *
from logs import *


logger = logging.getLogger('app.main')


# Запуск бота
if __name__ == '__main__':
    logger.info('The bot has been successfully launched')
    database_instance.connect()
    executor.start_polling(dispatcher=dp, skip_updates=True)
    logger.info('The bot has been successfully turned off')
    database_instance.close()
