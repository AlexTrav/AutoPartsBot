from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from db.database import database_instance

from db.repository import *


# User

# Проверка на наличие товара в корзине
def is_item_in_basket(auto_part_id: int, user_id: int) -> bool:
    entries = database_instance.return_select_query(f"SELECT * FROM basket WHERE user_id = {user_id} AND auto_part_id = {auto_part_id}")
    if entries:
        return True
    else:
        return False


# Возвращает клавиатуру в зависимости от состояния добавления
def get_add_kb_auto_part(kb: InlineKeyboardMarkup, cb: CallbackData, auto_part_id: int, user_id: int) -> InlineKeyboardMarkup:
    if not is_item_in_basket(auto_part_id, user_id):
        kb.add(InlineKeyboardButton(text='Добавить в корзину', callback_data=cb.new(id=auto_part_id, action='add_basket_count')))
    else:
        kb.add(InlineKeyboardButton(text='-', callback_data=cb.new(id=auto_part_id, action='dec_basket_count')), InlineKeyboardButton(text='+', callback_data=cb.new(id=auto_part_id, action='inc_basket_count')))
    return kb


# Оформляет заказ
def get_answer_place_in_order(user_id):
    entries = database_instance.return_select_query(f"SELECT * FROM basket WHERE user_id = {user_id} AND is_deleted = false")
    all_price = 0
    for entry in entries:
        auto_part = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE id = {entry[2]} AND is_deleted = false")[0]
        all_price += auto_part[6]
    int_current_datetime = datetime.now().strftime("%Y%m%d%H%M")
    order_id = place_in_order(user_id, int_current_datetime, all_price)
    for entry in entries:
        auto_part = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE id = {entry[2]} AND is_deleted = false")[0]
        basket_item = database_instance.return_select_query(f"SELECT * FROM basket WHERE id = {entry[0]} AND is_deleted = false")[0]
        place_in_order_item(order_id, user_id, auto_part[0], basket_item[3], auto_part[6])
    return 'Заказ успешно оформлен!'

