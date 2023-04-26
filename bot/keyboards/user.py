# Файл отправки клавиатур и сообщений пользователя

from bot.keyboards.pagination import *

from bot.keyboards.utils import *


# Отправить клавиатуру в зависимости от состояния
def get_keyboard(state, **kwargs):
    if state == 'UserStatesGroup:start':
        return get_start_kb(kwargs["user_id"])

    if state == 'UserStatesGroup:category_auto_parts':
        return get_category_auto_parts_kb()
    if state == 'UserStatesGroup:subcategory_auto_parts':
        return get_subcategory_auto_parts_kb(kwargs["category_id"])
    if state == 'UserStatesGroup:auto_parts':
        return get_auto_parts_kb(kwargs["subcategory_id"])

    if state == 'UserStatesGroup:cars_brands':
        return get_cars_brands_kb()
    if state == 'UserStatesGroup:cars_models':
        return get_cars_models_kb(kwargs["car_brand_id"])
    if state == 'UserStatesGroup:cars_submodels':
        return get_cars_submodels_kb(kwargs["car_model_id"])
    if state == 'UserStatesGroup:cars_modifications':
        return get_cars_modifications_kb(kwargs["car_submodel_id"])

    if state == 'UserStatesGroup:basket':
        return get_basket_kb(kwargs["user_id"])


# Клавиатура команды start
def get_start_kb(user_id):
    cb = CallbackData('main_menu', 'action')
    text = 'Добро пожаловать в Auto-Parts Bot!'
    start_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Каталог автозапчастей', callback_data=cb.new(action='category_auto_parts'))],
        [InlineKeyboardButton(text='Подбор автозапчастей', callback_data=cb.new(action='selection_auto_parts'))],
        [InlineKeyboardButton(text='Корзина', callback_data=cb.new(action='basket'))],
        [InlineKeyboardButton(text='Заказы', callback_data=cb.new(action='orders'))],
        [InlineKeyboardButton(text='Поиск', callback_data=cb.new(action='search'))],
        [InlineKeyboardButton(text='Профиль', callback_data=cb.new(action='profile'))],
        [InlineKeyboardButton(text='О нас', callback_data=cb.new(action='about'))]
    ])
    if database_instance.return_select_query(f'SELECT * FROM workers WHERE user_id = {user_id}'):
        start_kb.add(InlineKeyboardButton(text='Для работников', callback_data=cb.new(action='for_workers')))
    return text, start_kb


# Каталог автозапчастей

# Клавиатура каталога автозапчастей
def get_category_auto_parts_kb():
    cb = CallbackData('category_auto_parts', 'id', 'action')
    text = 'Выберите каталог автозапчастей:'
    category_auto_parts_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query("SELECT * FROM category_auto_parts WHERE is_deleted = false")
    for entry in entries:
        category_auto_parts_kb.add(InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='category')))
    category_auto_parts_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, category_auto_parts_kb


# Клавиатура подкаталога автозапчастей
def get_subcategory_auto_parts_kb(category_id):
    cb = CallbackData('subcategory_auto_parts', 'id', 'action')
    text = 'Выберите подкаталог автозапчастей:'
    subcategory_auto_parts_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query(f"SELECT * FROM subcategory_auto_parts WHERE category_id = {category_id} AND is_deleted = false")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            subcategory_auto_parts_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='subcategory')))
        subcategory_auto_parts_kb = add_pagination_to_kb(kb=subcategory_auto_parts_kb, cb=cb, len_data=len(entries), id_btn=category_id)
    else:
        for entry in entries:
            subcategory_auto_parts_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='subcategory')))
    subcategory_auto_parts_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, subcategory_auto_parts_kb


# Клавиатура автозапчастей
def get_auto_parts_kb(subcategory_id):
    cb = CallbackData('auto_parts', 'id', 'action')
    text = 'Выберите автозапчасть:'
    auto_parts_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE subcategory_id = {subcategory_id} AND count > 0 AND is_deleted = false")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            auto_parts_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='auto_part')))
        auto_parts_kb = add_pagination_to_kb(kb=auto_parts_kb, cb=cb, len_data=len(entries), id_btn=subcategory_id)
    else:
        for entry in entries:
            auto_parts_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='auto_part')))
    auto_parts_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, auto_parts_kb


# Клавиатура автозапчасти
def get_auto_part_kb(auto_part_id, user_id):
    cb = CallbackData('auto_part', 'id', 'action')
    entry = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE id = {auto_part_id} AND is_deleted = false")[0]
    subcategory = database_instance.return_select_query(f"SELECT * FROM subcategory_auto_parts WHERE id = {entry[1]}")[0]
    text = f'Наименвоание товара: {entry[2]}\n'
    if entry[3]:
        text += f'Производитель: {entry[3]}\n'
    if entry[4]:
        text += f'Артикул: {entry[4]}\n'
    if entry[5] and subcategory[1] != 1:
        text += f'Описание: {entry[5]}\n'
    text += f'------------------\nЦена: {entry[6]}₸\n------------------\n'
    text += f'Количество на складе: {entry[8]}\n'
    photo = entry[7]
    auto_part_kb = InlineKeyboardMarkup()
    auto_part_kb = get_add_kb_auto_part(auto_part_kb, cb, auto_part_id, user_id)
    auto_part_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, photo, auto_part_kb


# Подбор автозапчастей


# Клавиатура брэндов авто
def get_cars_brands_kb():
    cb = CallbackData('cars_brands', 'id', 'action')
    text = 'Мы осуществляем персональный подбор автозапчастей на следующие марки авто: BMW, AUDI, MERCEDES, VOLKSWAGEN\nДля подбора автозапчастей выберите марку авто:'
    cars_brands_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query("SELECT * FROM cars_brands WHERE is_deleted = false")
    for entry in entries:
        cars_brands_kb.add(InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='car_brand')))
    cars_brands_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, cars_brands_kb


# Клавиатура моделей авто
def get_cars_models_kb(car_brand_id):
    cb = CallbackData('cars_models', 'id', 'action')
    text = 'Выберите модель авто:'
    cars_models_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query(f"SELECT * FROM cars_models WHERE car_brand_id = {car_brand_id} AND is_deleted = false")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            cars_models_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='car_model')))
        cars_models_kb = add_pagination_to_kb(kb=cars_models_kb, cb=cb, len_data=len(entries), id_btn=car_brand_id)
    else:
        for entry in entries:
            cars_models_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='car_model')))
    cars_models_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, cars_models_kb


# Клавиатура конфигураций авто
def get_cars_submodels_kb(car_model_id):
    cb = CallbackData('cars_submodels', 'id', 'action')
    text = 'Выберите конфигурацию авто:'
    cars_submodels_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query(f"SELECT * FROM cars_submodels WHERE car_model_id = {car_model_id} AND is_deleted = false")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            cars_submodels_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='car_submodel')))
        cars_submodels_kb = add_pagination_to_kb(kb=cars_submodels_kb, cb=cb, len_data=len(entries), id_btn=car_model_id)
    else:
        for entry in entries:
            cars_submodels_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='car_submodel')))
    cars_submodels_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, cars_submodels_kb


# Клавиатура модификаций авто
def get_cars_modifications_kb(car_submodel_id):
    cb = CallbackData('cars_modifications', 'id', 'action')
    text = 'Выберите модификацию авто:'
    cars_modifications_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query(f"SELECT * FROM cars_modifications WHERE car_submodel_id = {car_submodel_id} AND is_deleted = false")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            cars_modifications_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='car_modification')))
        cars_modifications_kb = add_pagination_to_kb(kb=cars_modifications_kb, cb=cb, len_data=len(entries), id_btn=car_submodel_id)
    else:
        for entry in entries:
            cars_modifications_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='car_modification')))
    cars_modifications_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, cars_modifications_kb


# Клавиатура установки автозапчастей
def get_set_name_selection_auto_parts_kb():
    text = 'Введите наимновение запчасти/запчастей для выбраной модификации авто:'
    cb = CallbackData('set_name_selection_auto_parts', 'action')
    set_name_selection_auto_parts_kb = InlineKeyboardMarkup()
    set_name_selection_auto_parts_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, set_name_selection_auto_parts_kb


# Корзина

# Клавиатура корзины
def get_basket_kb(user_id):
    cb = CallbackData('basket', 'action')
    basket_kb = InlineKeyboardMarkup()
    text = 'Корзина:\n'
    entries = database_instance.return_select_query(f"SELECT * FROM basket WHERE user_id = {user_id} AND is_deleted = false")
    all_price, i = 0, 1
    for entry in entries:
        auto_part = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE id = {entry[2]} AND is_deleted = false")[0]
        if len(text) < 4093:
            text += f'{i}: Наименование: {auto_part[2]}; Количество: {entry[3]}; Цена: {auto_part[6]}₸\n'
        else:
            text += '...'
            break
        all_price += auto_part[6]
        i += 1
    if len(entries) > 0:
        text += f'Общая стоимость: {all_price}₸'
        basket_kb.add(InlineKeyboardButton(text='Оформить заказ', callback_data=cb.new(action='place_an_order')))
        basket_kb.add(InlineKeyboardButton(text='Редактировать корзину', callback_data=cb.new(action='update_basket')), InlineKeyboardButton(text='Очистить корзину', callback_data=cb.new(action='delete_basket')))
    basket_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, basket_kb


# Клавиатура редактирования корзины
def get_edit_basket_kb(user_id):
    cb = CallbackData('edit_basket', 'id', 'action')
    edit_basket_kb = InlineKeyboardMarkup()
    text = 'Редактирование корзины:'
    entries = database_instance.return_select_query(f"SELECT * FROM basket WHERE user_id = {user_id} AND is_deleted = false")
    for entry in entries:
        auto_part = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE id = {entry[2]} AND is_deleted = false")[0]
        edit_basket_kb.add(InlineKeyboardButton(text=auto_part[2], callback_data=cb.new(id=0, action='auto_part')), InlineKeyboardButton(text='Удалить', callback_data=cb.new(id=entry[0], action='delete_basket_item')))
    edit_basket_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, edit_basket_kb


# Заказы

# Клавиатура заказов
def get_orders_kb():
    pass


# Поиск

# Клавиатура поиска
def get_search_kb():
    pass


# Профиль

# Клавиатура профиля
def get_profile_kb():
    pass


# О нас

# Клавиатура  модуля "О нас"
def get_about_kb():
    pass
