# Файл состояний бота

from aiogram.dispatcher.filters.state import StatesGroup, State


# Состояния пользователя
class UserStatesGroup(StatesGroup):
    start = State()

    category_auto_parts = State()
    subcategory_auto_parts = State()
    auto_parts = State()
    auto_part = State()

    basket = State()
    edit_basket = State()

    orders = State()
    order = State()

    profile = State()

    search = State()

    about = State()


# Состояния менеджера
class ManagerStatesGroup(StatesGroup):
    start = State()


# Состояния курьера
class CourierStatesGroup(StatesGroup):
    start = State()
