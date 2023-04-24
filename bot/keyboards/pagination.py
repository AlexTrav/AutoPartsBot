from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData


main_page_entries = 10


def add_pagination_to_kb(kb: InlineKeyboardMarkup, cb: CallbackData, len_kb: int, id_btn: int) -> InlineKeyboardMarkup:
    if main_page_entries != 10:
        kb.add(InlineKeyboardButton(text='←', callback_data=cb.new(id=id_btn, action='left_page')))
    if main_page_entries < len_kb:
        kb.add(InlineKeyboardButton(text='→', callback_data=cb.new(id=id_btn, action='right_page')))
    return kb


def change_page(action: str):
    global main_page_entries
    if action == 'left_page':
        main_page_entries -= 10
    if action == 'right_page':
        main_page_entries += 10
