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

    if state == 'UserStatesGroup:orders':
        await UserStatesGroup.orders.set()

    if state == 'UserStatesGroup:search':
        await UserStatesGroup.search.set()
    if state == 'UserStatesGroup:search_by_name':
        await UserStatesGroup.search_by_name.set()
    if state == 'UserStatesGroup:search_by_article':
        await UserStatesGroup.search_by_article.set()
    if state == 'UserStatesGroup:search_auto_parts':
        await UserStatesGroup.search_auto_parts.set()

    if state == 'UserStatesGroup:profile':
        await UserStatesGroup.profile.set()
    if state == 'UserStatesGroup:edit_profile':
        await UserStatesGroup.edit_profile.set()


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
        reset_main_page_entries()
        await UserStatesGroup.orders.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_orders_kb(callback.from_user.id)
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
        text, kb = keyboards.user.get_profile_kb(callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'for_workers':
        await UserStatesGroup.for_workers.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_for_workers_kb(callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


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
        await message.answer('Ваша заявка успешно добавлена в базу! Ожидайте, скоро с вами свяжется модератор!')
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

# Обработчик заказов
@dp.callback_query_handler(CallbackData('orders', 'id', 'action').filter(), state=UserStatesGroup.orders)
async def orders(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        text, kb = keyboards.user.get_orders_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'order_items':
        await UserStatesGroup.order_items.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_order_items(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик заказа
@dp.callback_query_handler(CallbackData('order_items', 'id', 'action').filter(), state=UserStatesGroup.order_items)
async def orders(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'paid':
        answer = paid_order(callback.from_user.id, callback_data['id'])
        if answer == 'Заказ успешно оплачен! И отправлен на доставку!':
            text, kb = keyboards.user.get_order_items(callback_data['id'])
            await callback.message.edit_text(text=text,
                                             reply_markup=kb)
        await callback.answer(answer)
    if callback_data['action'] == 'delete_order':
        answer = delete_order(callback_data['id'])
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
        await callback.answer(answer)


# Поиск

# Обработчик поиска
@dp.callback_query_handler(CallbackData('search', 'action').filter(), state=UserStatesGroup.search)
async def search(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'search_by_name':
        await UserStatesGroup.search_by_name.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_search_by_name_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'search_by_article':
        await UserStatesGroup.search_by_article.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_search_by_article_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик возвращения из поиска по наименованию
@dp.callback_query_handler(CallbackData('search_by_name', 'action').filter(), state=UserStatesGroup.search_by_name)
async def back_search_by_name(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик возвращения из поиска по артиклу
@dp.callback_query_handler(CallbackData('search_by_article', 'action').filter(), state=UserStatesGroup.search_by_article)
async def back_search_by_article(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик получения сообщения поиска по наименованию
@dp.message_handler(content_types=['text'], state=UserStatesGroup.search_by_name)
async def search_by_name(message: types.Message, state: FSMContext):
    text, kb = keyboards.user.get_search_auto_parts_kb(message.text, 'name_lc')
    async with state.proxy() as data:
        data['search_message'] = message.text
        data['by'] = 'name_lc'
    if text != 'К сожалению записей не найдено':
        reset_main_page_entries()
        await UserStatesGroup.search_auto_parts.set()
        add_state(await state.get_state())
    await message.answer(text=text,
                         reply_markup=kb)


# Обработчик получения сообщения поиска по артиклу
@dp.message_handler(content_types=['text'], state=UserStatesGroup.search_by_article)
async def search_by_article(message: types.Message, state: FSMContext):
    text, kb = keyboards.user.get_search_auto_parts_kb(message.text, 'article')
    async with state.proxy() as data:
        data['search_message'] = message.text
        data['by'] = 'article'
    if text != 'К сожалению записей не найдено':
        reset_main_page_entries()
        await UserStatesGroup.search_auto_parts.set()
        add_state(await state.get_state())
    await message.answer(text=text,
                         reply_markup=kb)


# Обработчик не найденных автозапчастей
@dp.callback_query_handler(CallbackData('search_auto_parts', 'id', 'action').filter(), state=UserStatesGroup.search_by_name)
async def back_search_by_name(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик не найденных автозапчастей
@dp.callback_query_handler(CallbackData('search_auto_parts', 'id', 'action').filter(), state=UserStatesGroup.search_by_article)
async def back_search_by_article(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик найденных автозапчастей
@dp.callback_query_handler(CallbackData('search_auto_parts', 'id', 'action').filter(), state=UserStatesGroup.search_auto_parts)
async def search_auto_parts(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        async with state.proxy() as data:
            text, kb = keyboards.user.get_keyboard(STATES_LIST[-1], search_message=data['search_message'], by=data['by'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'search_auto_part':
        await UserStatesGroup.search_auto_part.set()
        add_state(await state.get_state())
        text, photo, kb = keyboards.user.get_auto_part_kb(callback_data['id'], callback.from_user.id)
        await callback.message.delete()
        await callback.message.answer_photo(photo=photo,
                                            caption=text,
                                            reply_markup=kb)


# Обработчик найденой автозапчасти
@dp.callback_query_handler(CallbackData('auto_part', 'id', 'action').filter(), state=UserStatesGroup.search_auto_part)
async def search_auto_part(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        await callback.message.delete()
        async with state.proxy() as data:
            text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], search_message=data['search_message'], by=data['by'])
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


# Профиль

# Обработчик профиля
@dp.callback_query_handler(CallbackData('profile', 'action').filter(), state=UserStatesGroup.profile)
async def profile(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'add_balance':
        await UserStatesGroup.add_balance.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_add_balance_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'update_profile':
        await UserStatesGroup.edit_profile.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_edit_profile_kb(callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик пополнения баланса
@dp.callback_query_handler(CallbackData('add_balance', 'action').filter(), state=UserStatesGroup.add_balance)
async def add_balance(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-1], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик редактирования профиля
@dp.callback_query_handler(CallbackData('update_profile', 'action').filter(), state=UserStatesGroup.edit_profile)
async def add_balance(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'set_phone' or callback_data['action'] == 'update_phone':
        await UserStatesGroup.add__update_phone.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_add__update_phone_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'set_address_delivery' or callback_data['action'] == 'update_address_delivery':
        await UserStatesGroup.add__update_address_delivery.set()
        add_state(await state.get_state())
        text, kb = keyboards.user.get_add__update_address_delivery_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик возвращения из редактирования телефона
@dp.callback_query_handler(CallbackData('set__update_phone', 'action').filter(), state=UserStatesGroup.add__update_phone)
async def back_add__update_phone(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик возвращения из редактирования адреса доставки
@dp.callback_query_handler(CallbackData('set__update_address_delivery', 'action').filter(), state=UserStatesGroup.add__update_address_delivery)
async def back_add__update_address_delivery(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик ожидающий сообщение с телефоном
@dp.message_handler(content_types=['text'], state=UserStatesGroup.add__update_phone)
async def add__update_phone(message: types.Message):
    if message.text.isdigit():
        if len(message.text) == 11:
            if message.text[0] == '8':
                update_phone(message.from_user.id, message.text)
                await message.answer('Номер телефон успешно изменён!')
                await UserStatesGroup.profile.set()
                text, kb = keyboards.user.get_profile_kb(message.from_user.id)
                await message.answer(text=text,
                                     reply_markup=kb)
                delete_state()
                delete_state()
            else:
                await message.answer('Не правильный ввод номера телефона! Формат: Номер должен начинаться с 8!')
        else:
            await message.answer('Не правильный ввод номера телефона! Формат: Номер состоит из 11 цифр!')
    else:
        await message.answer('Не правильный ввод номера телефона! Формат: Только цифры!')


# Обработчик ожидающий сообщение с адресом доставки
@dp.message_handler(content_types=['text'], state=UserStatesGroup.add__update_address_delivery)
async def add__update_phone(message: types.Message):
    if len(message.text) > 10:
        if len(message.text) < 200:
            update_address_delivery(message.from_user.id, message.text)
            await message.answer('Адрес доставки успешно изменён!')
            await UserStatesGroup.profile.set()
            text, kb = keyboards.user.get_profile_kb(message.from_user.id)
            await message.answer(text=text,
                                 reply_markup=kb)
            delete_state()
            delete_state()
        else:
            await message.answer('Не правильный ввод адреса доставки! Формат: Не более 200 символов!')
    else:
        await message.answer('Не правильный ввод адреса доставки! Формат: Не менее 10 символов!')


# Для работников

# Обработчик выбора входа
@dp.callback_query_handler(CallbackData('for_workers', 'action').filter(), state=UserStatesGroup.for_workers)
async def for_workers(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.user.get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'log_in_moderator':
        delete_all_states()
        change_role_id(callback.from_user.id, 2)
        await callback.message.delete()
        await callback.message.answer('Вы успешно зашли как модератор!')
    if callback_data['action'] == 'log_in_courier':
        delete_all_states()
        change_role_id(callback.from_user.id, 3)
        await callback.message.delete()
        await callback.message.answer('Вы успешно зашли как курьер!')
