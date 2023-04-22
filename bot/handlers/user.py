# Файл обработчик запросов пользователя

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

from bot.loader import dp

from bot.states import UserStatesGroup

from bot import keyboards
from db import repository


# Переключатель состояний
async def set_state():
    state = keyboards.STATES_LIST[-2]
    if state == 'UserStatesGroup:start':
        await UserStatesGroup.start.set()


# Обработчик главного меню
@dp.callback_query_handler(CallbackData('main_menu', 'action').filter(), state=UserStatesGroup.start)
async def main_menu(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'category_auto_parts':
        await UserStatesGroup.category_auto_parts.set()
        keyboards.add_state(await state.get_state())
        text, kb = keyboards.get_category_auto_parts_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'basket':
        await UserStatesGroup.basket.set()
        keyboards.add_state(await state.get_state())
        text, kb = keyboards.get_basket_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'orders':
        await UserStatesGroup.orders.set()
        keyboards.add_state(await state.get_state())
        text, kb = keyboards.get_orders_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'search':
        await UserStatesGroup.search.set()
        keyboards.add_state(await state.get_state())
        text, kb = keyboards.get_search_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'profile':
        await UserStatesGroup.profile.set()
        keyboards.add_state(await state.get_state())
        text, kb = keyboards.get_profile_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'about':
        await UserStatesGroup.about.set()
        keyboards.add_state(await state.get_state())
        text, kb = keyboards.get_about_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
