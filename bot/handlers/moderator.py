# Файл обработчик запросов модератора

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.loader import dp

from bot.states import ModeratorStatesGroup


from bot.keyboards.back_button import *

from bot import keyboards

from bot.keyboards.pagination import *

from db.repository import *


# Переключатель состояний
async def set_state():
    state = keyboards.STATES_LIST[-2]
    if state == 'ModeratorStatesGroup:start':
        await ModeratorStatesGroup.start.set()

    if state == 'ModeratorStatesGroup:selection_auto_parts':
        await ModeratorStatesGroup.selection_auto_parts.set()

    if state == 'ModeratorStatesGroup:users':
        await ModeratorStatesGroup.users.set()
    if state == 'ModeratorStatesGroup:add_balance_select_user':
        await ModeratorStatesGroup.add_balance_select_user.set()
    if state == 'ModeratorStatesGroup:set_roles_select_user':
        await ModeratorStatesGroup.set_roles_select_user.set()

    if state == 'ModeratorStatesGroup:datas':
        await ModeratorStatesGroup.datas.set()
    if state == 'ModeratorStatesGroup:data':
        await ModeratorStatesGroup.data.set()


# Обработчик главного меню
@dp.callback_query_handler(CallbackData('main_menu', 'action').filter(), state=ModeratorStatesGroup.start)
async def main_menu(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'selection_auto_parts':
        await ModeratorStatesGroup.selection_auto_parts.set()
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_selection_auto_parts_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'users':
        await ModeratorStatesGroup.users.set()
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_users_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'datas':
        await ModeratorStatesGroup.datas.set()
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_datas_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'documents':
        reset_main_page_entries()
        await ModeratorStatesGroup.documents.set()
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_documents_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'exit':
        delete_all_states()
        change_role_id(callback.from_user.id, 1)
        await callback.message.delete()
        await callback.message.answer('Вы успешно вышли!')


# Подбор автозапчастей

# Обработчик выбора заявки на подбор автозапчастей
@dp.callback_query_handler(CallbackData('selection_auto_parts', 'id', 'action').filter(), state=ModeratorStatesGroup.selection_auto_parts)
async def selection_application(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        text, kb = keyboards.moderator.get_selection_auto_parts_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'application':
        await ModeratorStatesGroup.application.set()
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_application_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик возвращения из заявки
@dp.callback_query_handler(CallbackData('application', 'action').filter(), state=ModeratorStatesGroup.application)
async def selection_application(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Пользователи


# Обработчик выбора действия для работы с пользователем
@dp.callback_query_handler(CallbackData('users', 'action').filter(), state=ModeratorStatesGroup.users)
async def selection_application(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'add_balance_select_user':
        await ModeratorStatesGroup.add_balance_select_user.set()
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_add_balance_select_user_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'set_roles_select_user':
        await ModeratorStatesGroup.set_roles_select_user.set()
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_set_roles_select_user_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик выбора пользователя для пополнения баланса
@dp.callback_query_handler(CallbackData('add_balance_select_user', 'id', 'action').filter(), state=ModeratorStatesGroup.add_balance_select_user)
async def select_user_add_balance(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        text, kb = keyboards.moderator.get_add_balance_select_user_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'user':
        await ModeratorStatesGroup.add_balance.set()
        async with state.proxy() as data:
            data['add_balance_user_id'] = callback_data['id']
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_add_balance_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик выбора пользователя для выдачи ролей
@dp.callback_query_handler(CallbackData('set_roles_select_user', 'id', 'action').filter(), state=ModeratorStatesGroup.set_roles_select_user)
async def select_user_set_roles(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        text, kb = keyboards.moderator.get_set_roles_select_user_kb()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'user':
        await ModeratorStatesGroup.set_roles.set()
        async with state.proxy() as data:
            data['set_roles_user_id'] = callback_data['id']
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_set_roles_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик возвращения из пополнения баланса пользователю
@dp.callback_query_handler(CallbackData('add_balance', 'action').filter(), state=ModeratorStatesGroup.add_balance)
async def back_add_balance(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик принимающий сообщение с суммой пополнения баланса пользователю
@dp.message_handler(content_types=['text'], state=ModeratorStatesGroup.add_balance)
async def add_balance_data(message: types.Message, state: FSMContext):
    if message.text.isdigit() and message.text.count('\n') == 0:
        async with state.proxy() as data:
            add_balance(data['add_balance_user_id'], message.text)
            await message.answer(f'Баланс успешно пополнен на сумму: {message.text} - пользователю: {data["add_balance_user_id"]}')
            await ModeratorStatesGroup.users.set()
            text, kb = keyboards.moderator.get_users_kb()
            await message.answer(text=text,
                                 reply_markup=kb)
            delete_state()
            delete_state()

    else:
        await message.answer('Ошибка ввода. Сумма должна состоять из цифр и без переносов строки!')


# Обработчик выдачи ролей пользователю
@dp.callback_query_handler(CallbackData('set_roles', 'action').filter(), state=ModeratorStatesGroup.set_roles)
async def set_roles_user(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'delete_role_moderator' or callback_data['action'] == 'add_role_moderator' or callback_data['action'] == 'delete_role_courier' or callback_data['action'] == 'add_role_courier':
        async with state.proxy() as data:
            get_role(data['set_roles_user_id'], callback_data['action'])
            await callback.answer('Успешно')
            text, kb = keyboards.moderator.get_set_roles_kb(data['set_roles_user_id'])
            await callback.message.edit_text(text=text,
                                             reply_markup=kb)


# Данные

# Обработчик выбора работы с данными
@dp.callback_query_handler(CallbackData('datas', 'action').filter(), state=ModeratorStatesGroup.datas)
async def select_data(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    else:
        reset_main_page_entries()
        await ModeratorStatesGroup.data.set()
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_data_kb(callback_data['action'])
        async with state.proxy() as data:
            data['action_datas'] = callback_data['action']
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик выбора записи или действия с данынми
@dp.callback_query_handler(CallbackData('data', 'id', 'action').filter(), state=ModeratorStatesGroup.data)
async def select_subdata(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_data_kb(data['action_datas'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'add_data':
        await ModeratorStatesGroup.add_data.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_add_data_kb(data['action_datas'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'subdata':
        await ModeratorStatesGroup.subdata.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['subdata_id'] = callback_data['id']
            text, kb = keyboards.moderator.get_subdata_kb(data['action_datas'], callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик возвращения из добавления записи данных
@dp.callback_query_handler(CallbackData('add_data', 'action').filter(), state=ModeratorStatesGroup.add_data)
async def back_add_data(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик принимающий сообщения для добавления записи данных
@dp.message_handler(content_types=['text'], state=ModeratorStatesGroup.add_data)
async def add_data(message: types.Message, state: FSMContext):
    pass


# Обработчик выбора действие с записью
@dp.callback_query_handler(CallbackData('subdata', 'action').filter(), state=ModeratorStatesGroup.subdata)
async def subdata(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2], action=data['action_datas'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == '':
        pass
    if callback_data['action'] == '':
        pass


# Обработчик выбора поля для редактирования записи данных
@dp.callback_query_handler(CallbackData('edit_subdata', 'action').filter(), state=ModeratorStatesGroup.edit_subdata)
async def edit_subdata(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2], action=data['action_datas'], subdata_id=data['subdata_id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    else:
        async with state.proxy() as data:
            data['edit_field'] = callback_data['action']
        pass


# Обработчик возвращения из редактирования поля записи данных
@dp.callback_query_handler(CallbackData('edit_field_subdata', 'action').filter(), state=ModeratorStatesGroup.edit_field_subdata)
async def back_edit_field_subdata(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2], action=data['action_datas'], subdata_id=data['subdata_id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик принимающий сообщения для редактирования поля записи данных
@dp.message_handler(content_types=['text'], state=ModeratorStatesGroup.edit_field_subdata)
async def add_data(message: types.Message, state: FSMContext):
    pass


# Документы
