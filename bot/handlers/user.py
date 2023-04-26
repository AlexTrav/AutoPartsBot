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

    if state == 'UserStatesGroup:cars_brands':
        await UserStatesGroup.cars_brands.set()
    if state == 'UserStatesGroup:cars_models':
        await UserStatesGroup.cars_models.set()
    if state == 'UserStatesGroup:cars_submodels':
        await UserStatesGroup.cars_submodels.set()
    if state == 'UserStatesGroup:cars_modifications':
        await UserStatesGroup.cars_modifications.set()

    if state == 'UserStatesGroup:basket':
        await UserStatesGroup.basket.set()


# Обработчик главного меню
@dp.callback_query_handler(CallbackData('main_menu', 'action').filter(), state=UserStatesGroup.start)
async def main_menu(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'category_auto_parts':
        await UserStatesGroup.category_auto_parts.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_category_auto_parts_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'selection_auto_parts':
        await UserStatesGroup.cars_brands.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_cars_brands_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'basket':
        await UserStatesGroup.basket.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_basket_kb(callback.from_user.id)
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
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
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
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
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
            text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], category_id=data['category_id'])
        await callback.message.edit_text(text=text,
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
            text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], subcategory_id=data['subcategory_id'])
        await callback.message.answer(text=text,
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


# Подбор автозапчастей

# Обработчик выбора марки авто
@dp.callback_query_handler(CallbackData('cars_brands', 'id', 'action').filter(), state=UserStatesGroup.cars_brands)
async def cars_brands(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'car_brand':
        reset_main_page_entries()
        await UserStatesGroup.cars_models.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['car_brand_id'] = callback_data['id']
        text, kb = keyboards.user.get_cars_models_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик выбора модели авто
@dp.callback_query_handler(CallbackData('cars_models', 'id', 'action').filter(), state=UserStatesGroup.cars_models)
async def cars_models(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        text, kb = keyboards.user.get_cars_models_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'car_model':
        reset_main_page_entries()
        await UserStatesGroup.cars_submodels.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['car_model_id'] = callback_data['id']
        text, kb = keyboards.user.get_cars_submodels_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик выбора конфигурации авто
@dp.callback_query_handler(CallbackData('cars_submodels', 'id', 'action').filter(), state=UserStatesGroup.cars_submodels)
async def cars_submodels(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], car_brand_id=data['car_brand_id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        text, kb = keyboards.user.get_cars_submodels_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'car_submodel':
        reset_main_page_entries()
        await UserStatesGroup.cars_modifications.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['car_submodel_id'] = callback_data['id']
        text, kb = keyboards.user.get_cars_modifications_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик выбора модификации авто
@dp.callback_query_handler(CallbackData('cars_modifications', 'id', 'action').filter(), state=UserStatesGroup.cars_modifications)
async def cars_modifications(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], car_model_id=data['car_model_id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        text, kb = keyboards.user.get_cars_modifications_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'car_modification':
        reset_main_page_entries()
        await UserStatesGroup.selection_auto_parts.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['car_modification_id'] = callback_data['id']
        text, kb = keyboards.user.get_set_name_selection_auto_parts_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик возвращения из формы установки автозапчастей
@dp.callback_query_handler(CallbackData('set_name_selection_auto_parts', 'action').filter(), state=UserStatesGroup.selection_auto_parts)
async def back_selection_auto_parts(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], car_submodel_id=data['car_submodel_id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик принимающий наименование запчасти/запчастей
@dp.message_handler(content_types=['text'], state=UserStatesGroup.selection_auto_parts)
async def set_name_selection_auto_parts_kb(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        add_selection_auto_parts(name=message.text, user_id=message.from_user.id, car_brand_id=data['car_brand_id'], car_model_id=data['car_model_id'], car_submodel_id=data['car_submodel_id'], car_modification_id=data['car_modification_id'])
        delete_all_states()
        await message.answer('Ваша заявка успешно добавлена в базу! Ожидайте, скоро с вами свяжется менеджер!')
        await UserStatesGroup.start.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_start_kb(message.from_user.id)
        await message.answer(text=text,
                             reply_markup=kb)


# Корзина

# Обработчик корзины
@dp.callback_query_handler(CallbackData('basket', 'action').filter(), state=UserStatesGroup.basket)
async def basket(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'place_an_order':
        answer = keyboards.utils.get_answer_place_in_order(callback.from_user.id)
        delete_from_user_basket(callback.from_user.id)
        await callback.answer(answer)
        text, kb = keyboards.user.get_basket_kb(callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'update_basket':
        await UserStatesGroup.edit_basket.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_edit_basket_kb(callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'delete_basket':
        delete_from_user_basket(callback.from_user.id)
        text, kb = keyboards.user.get_basket_kb(callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Редактирование корзины
@dp.callback_query_handler(CallbackData('edit_basket', 'id', 'action').filter(), state=UserStatesGroup.edit_basket)
async def edit_basket(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'auto_part':
        await callback.answer('Товар')
    if callback_data['action'] == 'delete_basket_item':
        delete_from_user_basket_item(callback_data['id'])
        text, kb = keyboards.user.get_edit_basket_kb(callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)



# Заказы

# Поиск

# Профиль

# О нас
