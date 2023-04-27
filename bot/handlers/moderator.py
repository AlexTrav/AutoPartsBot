# Файл обработчик запросов модератора

from aiogram import types

from bot.loader import dp

from bot.states import ModeratorStatesGroup

from bot import keyboards
from db import repository


# Переключатель состояний
async def set_state():
    state = keyboards.STATES_LIST[-2]
    if state == 'UserStatesGroup:start':
        await ModeratorStatesGroup.start.set()
