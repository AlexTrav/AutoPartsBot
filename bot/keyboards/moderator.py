# Файл отправки клавиатур и сообщений модератора

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.callback_data import CallbackData

# from db.database import database_instance


# Отправить клавиатуру в зависимости от состояния
def get_keyboard(state, **kwargs):
    if state == 'ModeratorStatesGroup:start':
        return get_start_kb()


# Клавиатура команды start
def get_start_kb():
    text = 'Модератор добро пожаловать в Auto-Parts Bot!'
    start_moderator_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='РАБОТА С ЗАКАЗАМИ', callback_data='work_products')],
        [InlineKeyboardButton(text='ВЫЙТИ', callback_data='exit')]
    ])
    return text, start_moderator_kb
