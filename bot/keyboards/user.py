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


# Клавиатура команды start
def get_start_kb(user_id):
    cb = CallbackData('main_menu', 'action')
    text = 'Добро пожаловать в Auto-Parts Bot!'
    start_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Каталог автозапчастей', callback_data=cb.new(action='category_auto_parts'))],
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
    entries = database_instance.return_select_query("SELECT * FROM category_auto_parts")
    for entry in entries:
        category_auto_parts_kb.add(InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='category')))
    category_auto_parts_kb.add(InlineKeyboardButton(text='Подбор автозапчастей', callback_data=cb.new(id=-1, action='selection_auto_parts')))
    category_auto_parts_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, category_auto_parts_kb


# Клавиатура подкаталога автозапчастей
def get_subcategory_auto_parts_kb(category_id):
    cb = CallbackData('subcategory_auto_parts', 'id', 'action')
    text = 'Выберите подкаталог автозапчастей:'
    subcategory_auto_parts_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query(f"SELECT * FROM subcategory_auto_parts WHERE category_id = {category_id}")
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
    entries = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE subcategory_id = {subcategory_id} AND count > 0")
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
    entry = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE id = {auto_part_id}")[0]
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


# Корзина

# Клавиатура корзины
def get_basket_kb():
    pass


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
