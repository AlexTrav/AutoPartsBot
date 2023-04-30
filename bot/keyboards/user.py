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

    if state == 'UserStatesGroup:orders':
        return get_orders_kb(kwargs["user_id"])

    if state == 'UserStatesGroup:search':
        return get_search_kb()
    if state == 'UserStatesGroup:search_by_name':
        return get_search_by_name_kb()
    if state == 'UserStatesGroup:search_by_article':
        return get_search_by_article_kb()

    if state == 'UserStatesGroup:search_auto_parts':
        return get_search_auto_parts_kb(kwargs['search_message'], kwargs['by'])

    if state == 'UserStatesGroup:profile':
        return get_profile_kb(kwargs['user_id'])
    if state == 'UserStatesGroup:edit_profile':
        return get_edit_profile_kb(kwargs['user_id'])


# Клавиатура команды start
def get_start_kb(user_id):
    cb = CallbackData('main_menu', 'action')
    text = 'Добро пожаловать в Auto-Parts Bot!'
    start_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Каталог автозапчастей', callback_data=cb.new(action='category_auto_parts'))],
        [InlineKeyboardButton(text='Подбор автозапчастей', callback_data=cb.new(action='selection_auto_parts'))],
        [InlineKeyboardButton(text='Поиск автозапчастей', callback_data=cb.new(action='search'))],
        [InlineKeyboardButton(text='Профиль', callback_data=cb.new(action='profile'))],
        [InlineKeyboardButton(text='Корзина', callback_data=cb.new(action='basket'))],
        [InlineKeyboardButton(text='Заказы', callback_data=cb.new(action='orders'))],
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
def get_orders_kb(user_id):
    cb = CallbackData('orders', 'id', 'action')
    orders_kb = InlineKeyboardMarkup()
    text = 'Заказы\nВыберите заказ:'
    entries = database_instance.return_select_query(f"SELECT * FROM orders WHERE user_id = {user_id} AND is_deleted = false")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            reg_date = str(entry[2])[6:8] + '.' + str(entry[2])[4:6] + '.' + str(entry[2])[2:4] + ' ' + str(entry[2])[8:10] + ':' + str(entry[2])[10:]
            orders_kb.add(InlineKeyboardButton(text=reg_date, callback_data=cb.new(id=entry[0], action='order_items')))
        orders_kb = add_pagination_to_kb(kb=orders_kb, cb=cb, len_data=len(entries), id_btn=user_id)
    else:
        for entry in entries:
            reg_date = str(entry[2])[6:8] + '.' + str(entry[2])[4:6] + '.' + str(entry[2])[2:4] + ' ' + str(entry[2])[8:10] + ':' + str(entry[2])[10:]
            orders_kb.add(InlineKeyboardButton(text=reg_date, callback_data=cb.new(id=entry[0], action='order_items')))
    orders_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, orders_kb


# Клавиатура заказа
def get_order_items(order_id):
    cb = CallbackData('order_items', 'id', 'action')
    order_items_kb = InlineKeyboardMarkup()
    text = f'Заказ под номером: {order_id}\n'
    order = database_instance.return_select_query(f"SELECT * FROM orders WHERE id = {order_id} AND is_deleted = false")[0]
    entries = database_instance.return_select_query(f"SELECT * FROM orders_items WHERE order_id = {order_id} AND is_deleted = false")
    all_price, i = 0, 1
    for entry in entries:
        auto_part = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE id = {entry[3]} AND is_deleted = false")[0]
        text += f'{i}: Наименование: {auto_part[2]}; Количество: {entry[4]}; Цена: {entry[5]}₸\n'
        all_price += entry[5]
        i += 1
    is_paid = 'Оплачен' if order[3] else 'Не оплачен'
    is_delivered = 'Доставлен' if order[4] else 'Не доставлен'
    text += f'Статус оплаты: {is_paid}\n'
    text += f'Статус доставки: {is_delivered}\n'
    text += f'Общая стоимость: {all_price}₸\n'
    if not order[3]:
        order_items_kb.add(InlineKeyboardButton(text='Оплатить', callback_data=cb.new(id=order_id, action='paid')))
        order_items_kb.add(InlineKeyboardButton(text='Удалить заказ', callback_data=cb.new(id=order_id, action='delete_order')))
    order_items_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, order_items_kb


# Поиск

# Клавиатура поиска
def get_search_kb():
    cb = CallbackData('search', 'action')
    text = 'Поиск автозапчастей\nВыберите тип поиска:'
    search_kb = InlineKeyboardMarkup()
    search_kb.add(InlineKeyboardButton(text='Поиск по наименованию', callback_data=cb.new(action='search_by_name')))
    search_kb.add(InlineKeyboardButton(text='Поиск по артиклу', callback_data=cb.new(action='search_by_article')))
    search_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, search_kb


# Клавиатура поиска по наименованию
def get_search_by_name_kb():
    cb = CallbackData('search_by_name', 'action')
    text = 'Введите наименование автозапчасти:'
    search_by_name_kb = InlineKeyboardMarkup()
    search_by_name_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, search_by_name_kb


# Клавиатура поиска по артиклу
def get_search_by_article_kb():
    cb = CallbackData('search_by_article', 'action')
    text = 'Введите артикул автозапчасти:'
    search_by_article_kb = InlineKeyboardMarkup()
    search_by_article_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, search_by_article_kb


# Клавиатура результата поиска
def get_search_auto_parts_kb(search_message, by):
    cb = CallbackData('search_auto_parts', 'id', 'action')
    search_auto_parts_by_name_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE {by} LIKE '%{search_message.lower()}%' AND count > 0 AND is_deleted = false")
    if len(entries) > 0:
        text = f'Найдено автозапчастей: {len(entries)}\n'
        if len(entries) > 10:
            for entry in entries[MainPage.entries - 10:MainPage.entries]:
                search_auto_parts_by_name_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='search_auto_part')))
            search_auto_parts_by_name_kb = add_pagination_to_kb(kb=search_auto_parts_by_name_kb, cb=cb, len_data=len(entries), id_btn=search_message)
        else:
            for entry in entries:
                search_auto_parts_by_name_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='search_auto_part')))
    else:
        text = 'К сожалению записей не найдено'
    search_auto_parts_by_name_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, search_auto_parts_by_name_kb


# Профиль

# Клавиатура профиля
def get_profile_kb(user_id):
    cb = CallbackData('profile', 'action')
    user = database_instance.return_select_query(f"SELECT * FROM users WHERE id = {user_id}")[0]
    phone = user[3] if user[3] else 'Не указан'
    address_delivery = user[6] if user[6] else 'Не указан'
    text = f'Профиль пользователя: {user[0]}\nПолное имя: {user[1]}\nТелефон: {phone}\nАдрес доставки: {address_delivery}\nБаланс: {user[7]}₸'
    profile_kb = InlineKeyboardMarkup()
    profile_kb.add(InlineKeyboardButton(text='Редактировать профиль', callback_data=cb.new(action='update_profile')))
    profile_kb.add(InlineKeyboardButton(text='Пополнить баланс', callback_data=cb.new(action='add_balance')))
    profile_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, profile_kb


# Клавиатура пополнения баланса
def get_add_balance_kb():
    cb = CallbackData('add_balance', 'action')
    text = 'Для пополнения баланса, обратитесь к одному из модераторов:'
    add_balance_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query("SELECT * FROM workers WHERE role_id = 2")
    if len(entries) > 10:
        for entry in entries:
            user = database_instance.return_select_query(f"SELECT * FROM users WHERE id = {entry[0]}")[0]
            url = f'https://t.me/{user[2]}'
            add_balance_kb.add(InlineKeyboardButton(text=user[1], url=url))
        add_balance_kb = add_pagination_to_kb(kb=add_balance_kb, cb=cb, len_data=len(entries), id_btn=0)
    else:
        for entry in entries:
            user = database_instance.return_select_query(f"SELECT * FROM users WHERE id = {entry[0]}")[0]
            url = f'https://t.me/{user[2]}'
            add_balance_kb.add(InlineKeyboardButton(text=user[1], url=url))
    add_balance_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, add_balance_kb


# Клавиатура редактирования профиля
def get_edit_profile_kb(user_id):
    cb = CallbackData('update_profile', 'action')
    text = 'Выберите действие:'
    user = database_instance.return_select_query(f"SELECT * FROM users WHERE id = {user_id}")[0]
    edit_profile_kb = InlineKeyboardMarkup()
    if not user[3]:
        edit_profile_kb.add(InlineKeyboardButton(text='Установить телефон', callback_data=cb.new(action='set_phone')))
    else:
        edit_profile_kb.add(InlineKeyboardButton(text='Поменять телефон', callback_data=cb.new(action='update_phone')))
    if not user[6]:
        edit_profile_kb.add(InlineKeyboardButton(text='Установить адрес доставки', callback_data=cb.new(action='set_address_delivery')))
    else:
        edit_profile_kb.add(InlineKeyboardButton(text='Поменять адрес доставки', callback_data=cb.new(action='update_address_delivery')))
    edit_profile_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, edit_profile_kb


# Клавиатура ввода телефона
def get_add__update_phone_kb():
    cb = CallbackData('set__update_phone', 'action')
    text = 'Введите телефон:\nФормат: Только цифры\nПример: 87776665544'
    add_update_phone_kb = InlineKeyboardMarkup()
    add_update_phone_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, add_update_phone_kb


# Клавиатура ввода адреса
def get_add__update_address_delivery_kb():
    cb = CallbackData('set__update_address_delivery', 'action')
    text = 'Введите адрес доставки:\nФормат: Не более 200 символов'
    add_update_address_delivery = InlineKeyboardMarkup()
    add_update_address_delivery.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, add_update_address_delivery


# Для работников

# Клавиатура выбора захода
def get_for_workers_kb(user_id):
    cb = CallbackData('for_workers', 'action')
    text = 'Выберите действие:'
    for_workers_kb = InlineKeyboardMarkup()
    if database_instance.return_select_query(f"SELECT * FROM workers WHERE user_id = {user_id} and role_id = 2"):
        for_workers_kb.add(InlineKeyboardButton(text='Зайти как модератор', callback_data=cb.new(action='log_in_moderator')))
    if database_instance.return_select_query(f"SELECT * FROM workers WHERE user_id = {user_id} and role_id = 3"):
        for_workers_kb.add(InlineKeyboardButton(text='Зайти как курьер', callback_data=cb.new(action='log_in_courier')))
    for_workers_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, for_workers_kb

