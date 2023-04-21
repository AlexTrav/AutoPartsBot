# Файл отправки клавиатур и сообщений курьера

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.callback_data import CallbackData

# from db.database import database_instance


# Клавиатура команды start
def get_start_kb():
    text = 'Курьер добро пожаловать в Auto-Parts Bot!'
    start_manager_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='РАБОТА С ЗАКАЗАМИ', callback_data='work_products')],
        [InlineKeyboardButton(text='ВЫЙТИ', callback_data='exit')]
    ])
    return text, start_manager_kb
