# Файл обработчик запросов курьера

from aiogram import types

from bot.loader import dp

from bot.states import CourierStatesGroup

from bot import keyboards
from db import repository


# Переключатель состояний
async def set_state():
    state = keyboards.STATES_LIST[-2]
    if state == 'UserStatesGroup:start':
        await CourierStatesGroup.start.set()
