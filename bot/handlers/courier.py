# Файл обработчик запросов курьера

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import keyboards
from bot.keyboards.back_button import *
from bot.keyboards.pagination import *
from bot.loader import dp
from bot.states import CourierStatesGroup
from db.repository import *


# Переключатель состояний
async def set_state():
    state = keyboards.STATES_LIST[-2]
    if state == 'CourierStatesGroup:start':
        await CourierStatesGroup.start.set()

    if state == 'CourierStatesGroup:orders_for_delivery':
        await CourierStatesGroup.orders_for_delivery.set()


# Обработчик главного меню
@dp.callback_query_handler(CallbackData('main_menu', 'action').filter(), state=CourierStatesGroup.start)
async def main_menu(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'orders_for_delivery':
        await CourierStatesGroup.orders_for_delivery.set()
        add_state(await state.get_state())
        text, kb = keyboards.courier.get_orders_for_delivery_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'exit':
        delete_all_states()
        change_role_id(callback.from_user.id, 1)
        await callback.message.delete()
        await callback.message.answer('Вы успешно вышли!')


# Заказы на доставку

# Обработчик выбора заказа на доставку
@dp.callback_query_handler(CallbackData('orders_for_delivery', 'id', 'action').filter(), state=CourierStatesGroup.orders_for_delivery)
async def orders_for_delivery(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.courier.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'order_for_delivery':
        await CourierStatesGroup.order_for_delivery.set()
        add_state(await state.get_state())
        text, kb = keyboards.courier.get_order_for_delivery_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обрабочтик действий с заказом на доставку
@dp.callback_query_handler(CallbackData('order_for_delivery', 'id', 'action').filter(), state=CourierStatesGroup.order_for_delivery)
async def order_for_delivery(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.courier.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'delivered_order':
        delivered_order(callback.from_user.id, callback_data['id'])
        await CourierStatesGroup.orders_for_delivery.set()
        await callback.answer('Заказ успешно доставлен')
        delete_state()
        text, kb = keyboards.courier.get_orders_for_delivery_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
