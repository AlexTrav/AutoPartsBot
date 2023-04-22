# Файл отправки клавиатур и сообщений пользователя

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# from db.database import database_instance


# Отправить клавиатуру в зависимости от состояния
def get_keyboard(state, **kwargs):
    if state == 'UserStatesGroup:start':
        return get_start_kb()


# Клавиатура команды start
def get_start_kb():
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
    return text, start_kb


# Клавиатура каталога автозапчастей
def get_category_auto_parts_kb():
    pass


# Клавиатура корзины
def get_basket_kb():
    pass


# Клавиатура заказов
def get_orders_kb():
    pass


# Клавиатура поиска
def get_search_kb():
    pass


# Клавиатура профиля
def get_profile_kb():
    pass


# Клавиатура  модуля "О нас"
def get_about_kb():
    pass


