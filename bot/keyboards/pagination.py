from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData


class MainPage:

    entries = 10


def add_pagination_to_kb(kb: InlineKeyboardMarkup, cb: CallbackData, len_data: int, id_btn: int) -> InlineKeyboardMarkup:
    if MainPage.entries != 10 and MainPage.entries < len_data:
        kb.add(InlineKeyboardButton(text='←', callback_data=cb.new(id=id_btn, action='left_page')), (InlineKeyboardButton(text='→', callback_data=cb.new(id=id_btn, action='right_page'))))
    else:
        if MainPage.entries != 10:
            kb.add(InlineKeyboardButton(text='←', callback_data=cb.new(id=id_btn, action='left_page')))
        if MainPage.entries < len_data:
            kb.add(InlineKeyboardButton(text='→', callback_data=cb.new(id=id_btn, action='right_page')))
    return kb


def change_page(action: str):
    if action == 'left_page':
        MainPage.entries -= 10
    if action == 'right_page':
        MainPage.entries += 10


def reset_main_page_entries():
    MainPage.entries = 10
