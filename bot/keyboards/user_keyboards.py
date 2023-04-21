# Файл отправки клавиатур и сообщений пользователя

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.callback_data import CallbackData

# from db.database import database_instance


# Клавиатура команды start
def get_start_kb():
    text = 'Добро пожаловать в Auto-Parts Bot!'
    start_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='КАТАЛОГ АВТОЗАПЧАСТЕЙ', callback_data='1')],
        [InlineKeyboardButton(text='СОПУТСВУЮЩИЕ ТОВАРЫ', callback_data='2')],
        [InlineKeyboardButton(text='ПОИСК', callback_data='search')],
        [InlineKeyboardButton(text='ПРОФИЛЬ', callback_data='profile')],
        [InlineKeyboardButton(text='КОРЗИНА', callback_data='basket')],
        [InlineKeyboardButton(text='О НАС', callback_data='about')]
    ])
    return text, start_kb
