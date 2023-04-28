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
    order_items = State()

    profile = State()
    edit_profile = State()

    add_balance = State()

    add__update_phone = State()
    add__update_address_delivery = State()

    search = State()
    search_by_name = State()
    search_by_article = State()

    search_auto_parts = State()
    search_auto_part = State()

    for_workers = State()


# Состояния модератора
class ModeratorStatesGroup(StatesGroup):
    start = State()

    selection_auto_parts = State()
    application = State()

    users = State()
    add_balance_select_user = State()
    set_roles_select_user = State()
    add_balance = State()
    set_roles = State()

    datas = State()

    data = State()
    add_data = State()
    subdata = State()
    edit_subdata = State()
    edit_field_subdata = State()

    # category_auto_parts = State()
    # add_category_auto_part = State()
    # category_auto_part = State()
    # edit_category_auto_part = State()
    # edit_field_category_auto_part = State()

    # subcategory_auto_parts = State()
    # add_subcategory_auto_part = State()
    # subcategory_auto_part = State()
    # edit_subcategory_auto_part = State()
    # edit_field_subcategory_auto_part = State()

    # auto_parts = State()
    # add_auto_part = State()
    # auto_part = State()
    # edit_auto_part = State()
    # edit_field_auto_part = State()

    # cars_brands = State()
    # add_car_brand = State()
    # car_brand = State()
    # edit_car_brand = State()
    # edit_field_car_brand = State()

    # cars_models = State()
    # add_car_model = State()
    # car_model = State()
    # edit_car_model = State()
    # edit_field_car_model = State()

    # cars_submodels = State()
    # add_car_submodel = State()
    # car_submodel = State()
    # edit_car_submodel = State()
    # edit_field_car_submodel = State()

    # cars_modifications = State()
    # add_car_modification = State()
    # car_modification = State()
    # edit_car_modification = State()
    # edit_field_car_modification = State()

    documents = State()
    document = State()


# Состояния курьера
class CourierStatesGroup(StatesGroup):
    start = State()
