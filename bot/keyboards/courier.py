# Файл отправки клавиатур и сообщений курьера

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

from bot.keyboards import MainPage, add_pagination_to_kb
from db.database import database_instance


# Отправить клавиатуру в зависимости от состояния
def get_keyboard(state):
    if state == 'CourierStatesGroup:start':
        return get_start_kb()

    if state == 'CourierStatesGroup:orders_for_delivery':
        return get_orders_for_delivery_kb()


# Клавиатура команды start
def get_start_kb():
    cb = CallbackData('main_menu', 'action')
    text = 'Курьер добро пожаловать в Auto-Parts Bot!'
    start_moderator_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Заказы на доставку', callback_data=cb.new(action='orders_for_delivery'))],
        [InlineKeyboardButton(text='Выйти', callback_data=cb.new(action='exit'))]
    ])
    return text, start_moderator_kb


# Заказы на доставку

# Клавиатура заказов на доставку
def get_orders_for_delivery_kb():
    cb = CallbackData('orders_for_delivery', 'id', 'action')
    text = 'Выберите заказ на доставку:'
    entries = database_instance.return_select_query(f"SELECT * FROM delivery where is_deleted = false AND is_completed = false")
    orders_for_delivery_kb = InlineKeyboardMarkup()
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            order = database_instance.return_select_query(f"SELECT * FROM orders WHERE id = {entry[1]} AND is_deleted = false")[0]
            reg_date = str(order[2])[6:8] + '.' + str(order[2])[4:6] + '.' + str(order[2])[2:4] + ' ' + str(order[2])[8:10] + ':' + str(order[2])[10:]
            orders_for_delivery_kb.add(InlineKeyboardButton(text=reg_date, callback_data=cb.new(id=entry[1], action='order_for_delivery')))
        orders_for_delivery_kb = add_pagination_to_kb(kb=orders_for_delivery_kb, cb=cb, len_data=len(entries), id_btn=0)
    else:
        for entry in entries:
            order = database_instance.return_select_query(f"SELECT * FROM orders WHERE id = {entry[1]} AND is_deleted = false")[0]
            reg_date = str(order[2])[6:8] + '.' + str(order[2])[4:6] + '.' + str(order[2])[2:4] + ' ' + str(order[2])[8:10] + ':' + str(order[2])[10:]
            orders_for_delivery_kb.add(InlineKeyboardButton(text=reg_date, callback_data=cb.new(id=entry[1], action='order_for_delivery')))
    orders_for_delivery_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, orders_for_delivery_kb


# Клавиатура заказа на доставку
def get_order_for_delivery_kb(order_id):
    cb = CallbackData('order_for_delivery', 'id', 'action')
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
    user = database_instance.return_select_query(f"SELECT * FROM users WHERE id = {order[1]}")[0]
    url = f'https://t.me/{user[2]}'
    text += f'Данные пользователя:\nКлюч пользователя: {user[0]}\nПользователь: {user[1]}\nНомер телефона: {user[3]}\nАдрес доставки: {user[6]}\nСсылка на пользователя: {url}'
    order_for_delivery_kb = InlineKeyboardMarkup()
    order_for_delivery_kb.add(InlineKeyboardButton(text='Доставил заказ', callback_data=cb.new(id=order_id, action='delivered_order')))
    order_for_delivery_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, order_for_delivery_kb
