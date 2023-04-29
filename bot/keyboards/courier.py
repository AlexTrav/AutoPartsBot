# Файл отправки клавиатур и сообщений курьера

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.callback_data import CallbackData

# from db.database import database_instance


# Отправить клавиатуру в зависимости от состояния
from aiogram.utils.callback_data import CallbackData


def get_keyboard(state, **kwargs):
    if state == 'CourierStatesGroup:start':
        return get_start_kb()


# Клавиатура команды start
def get_start_kb():
    cb = CallbackData('main_menu', 'action')
    text = 'Курьер добро пожаловать в Auto-Parts Bot!'
    start_moderator_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Заказы на доставку', callback_data='orders_for_delivery')],
        [InlineKeyboardButton(text='Выйти', callback_data='exit')]
    ])
    return text, start_moderator_kb
