# Файл состояний бота

from aiogram.dispatcher.filters.state import StatesGroup, State


# Состояния пользователя
class UserStatesGroup(StatesGroup):
    start = State()

    category_auto_parts = State()
    subcategory_auto_parts = State()
    auto_parts = State()
    auto_part = State()

    cars_brands = State()
    cars_models = State()
    cars_submodels = State()
    cars_modifications = State()
    selection_auto_parts = State()

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
