# Файл состояний бота

from aiogram.dispatcher.filters.state import StatesGroup, State


# Состояния пользователя
class UserStatesGroup(StatesGroup):
    start = State()


# Состояния менеджера
class ManagerStatesGroup(StatesGroup):
    start = State()


# Состояния курьера
class CourierStatesGroup(StatesGroup):
    start = State()
