# Файл обработчик запросов пользователя

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.loader import dp

from bot.states import UserStatesGroup

from bot.keyboards.back_button import *

from bot import keyboards

from bot.keyboards.pagination import *

from db.repository import *


# Переключатель состояний
async def set_state():
    state = keyboards.STATES_LIST[-2]
    if state == 'UserStatesGroup:start':
        await UserStatesGroup.start.set()

    if state == 'UserStatesGroup:category_auto_parts':
        await UserStatesGroup.category_auto_parts.set()
    if state == 'UserStatesGroup:subcategory_auto_parts':
        await UserStatesGroup.subcategory_auto_parts.set()
    if state == 'UserStatesGroup:auto_parts':
        await UserStatesGroup.auto_parts.set()


# Обработчик главного меню
@dp.callback_query_handler(CallbackData('main_menu', 'action').filter(), state=UserStatesGroup.start)
async def main_menu(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'category_auto_parts':
        await UserStatesGroup.category_auto_parts.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_category_auto_parts_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'basket':
        await UserStatesGroup.basket.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_basket_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'orders':
        await UserStatesGroup.orders.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_orders_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'search':
        await UserStatesGroup.search.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_search_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'profile':
        await UserStatesGroup.profile.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_profile_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'about':
        await UserStatesGroup.about.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_about_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'for_workers':
        pass


# Каталог автозапчастей

# Обработчик каталога автозапчастей
@dp.callback_query_handler(CallbackData('category_auto_parts', 'id', 'action').filter(), state=UserStatesGroup.category_auto_parts)
async def category_auto_parts(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'selection_auto_parts':
        pass
    if callback_data['action'] == 'category':
        await UserStatesGroup.subcategory_auto_parts.set()
        add_state(await state.get_state())
        reset_main_page_entries()
        async with state.proxy() as data:
            data['category_id'] = callback_data['id']
        text, kb = keyboards.user.get_subcategory_auto_parts_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик подкаталога автозапчастей
@dp.callback_query_handler(CallbackData('subcategory_auto_parts', 'id', 'action').filter(), state=UserStatesGroup.subcategory_auto_parts)
async def subcategory_auto_parts(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = keyboards.user.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        text, kb = keyboards.user.get_subcategory_auto_parts_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'subcategory':
        await UserStatesGroup.auto_parts.set()
        async with state.proxy() as data:
            data['subcategory_id'] = callback_data['id']
        add_state(await state.get_state())
        reset_main_page_entries()
        text, kb = keyboards.user.get_auto_parts_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик автозапчастей
@dp.callback_query_handler(CallbackData('auto_parts', 'id', 'action').filter(), state=UserStatesGroup.auto_parts)
async def auto_parts(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            ans, kb = keyboards.user.get_keyboard(STATES_LIST[-2], category_id=data['category_id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        text, kb = keyboards.user.get_auto_parts_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'auto_part':
        await UserStatesGroup.auto_part.set()
        await callback.message.delete()
        add_state(await state.get_state())
        text, photo, kb = keyboards.user.get_auto_part_kb(callback_data['id'], callback.from_user.id)
        await callback.message.answer_photo(photo=photo,
                                            caption=text,
                                            reply_markup=kb)


# Обработчик автозапчасти
@dp.callback_query_handler(CallbackData('auto_part', 'id', 'action').filter(), state=UserStatesGroup.auto_part)
async def auto_part(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        await callback.message.delete()
        async with state.proxy() as data:
            ans, kb = keyboards.user.get_keyboard(STATES_LIST[-2], subcategory_id=data['subcategory_id'])
        await callback.message.answer(text=ans,
                                      reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'add_basket_count' or callback_data['action'] == 'inc_basket_count' or callback_data['action'] == 'dec_basket_count':
        answer = add_basket_auto_part(action=callback_data['action'], user_id=callback.from_user.id, auto_part_id=callback_data['id'])
        await callback.answer(answer)
        await callback.message.delete()
        text, photo, kb = keyboards.user.get_auto_part_kb(callback_data['id'], callback.from_user.id)
        await callback.message.answer_photo(photo=photo,
                                            caption=text,
                                            reply_markup=kb)


# Корзина

# Заказы

# Поиск

# Профиль

# О нас
