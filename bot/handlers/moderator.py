# Файл обработчик запросов модератора
from datetime import datetime

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
    if state == 'ModeratorStatesGroup:add_data':
        await ModeratorStatesGroup.add_data.set()

    if state == 'ModeratorStatesGroup:documents_types':
        await ModeratorStatesGroup.documents_types.set()
    if state == 'ModeratorStatesGroup:documents':
        await ModeratorStatesGroup.documents.set()


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
        await ModeratorStatesGroup.documents_types.set()
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_documents_types_kb()
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
async def back_add_data(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2], action=data['action_datas'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Обработчик принимающий сообщения для добавления записи данных
@dp.message_handler(content_types=['text'], state=ModeratorStatesGroup.add_data)
async def add_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['action_datas'] == 'category_auto_parts' or data['action_datas'] == 'cars_brands':
            if message.text.count('\n') == 0:
                message_data = [message.text]
                add_data_repository(table=data['action_datas'], key=0, data=message_data)
                await message.answer('Успешно')
                delete_state()
                await ModeratorStatesGroup.data.set()
                text, kb = keyboards.moderator.get_data_kb(data['action_datas'])
                await message.answer(text=text,
                                     reply_markup=kb)
            else:
                await message.answer('Неверный ввод данных!')
        if data['action_datas'] == 'subcategory_auto_parts' or data['action_datas'] == 'cars_models' or data['action_datas'] == 'cars_submodels' or data['action_datas'] == 'cars_modifications':
            if message.text.count('\n') == 0:
                message_data = [message.text]
                data['message_data'] = message_data
                await ModeratorStatesGroup.set_key_for_add_data.set()
                add_state(await state.get_state())
                text, kb = keyboards.moderator.get_set_key_for_add_data_kb(data['action_datas'])
                await message.answer(text=text,
                                     reply_markup=kb)
            else:
                await message.answer('Неверный ввод данных!')
        if data['action_datas'] == 'auto_parts':
            if message.text.count('\n') == 6:
                message_data = message.text.split('\n')
                if message_data[4].isdigit() and message_data[6].isdigit():
                    data['message_data'] = message_data
                    await ModeratorStatesGroup.set_key_for_add_data.set()
                    add_state(await state.get_state())
                    text, kb = keyboards.moderator.get_set_key_for_add_data_kb(data['action_datas'])
                    await message.answer(text=text,
                                         reply_markup=kb)
                else:
                    await message.answer('Неверный ввод данных, цена и количество должны быть числом!')
            else:
                await message.answer('Неверный ввод данных!')


# Обработчик выбора ключа для добавления данных
@dp.callback_query_handler(CallbackData('set_key_for_add_data', 'id', 'action').filter(), state=ModeratorStatesGroup.set_key_for_add_data)
async def set_key_for_add_data(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2], action=data['action_datas'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_set_key_for_add_data_kb(data['action_datas'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'key':
        async with state.proxy() as data:
            add_data_repository(table=data['action_datas'], key=callback_data['id'], data=data['message_data'])
            if data['action_datas'] == 'auto_parts':
                auto_part = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE name = '{data['message_data'][0]}'")[0]
                invoice_date = datetime.now().strftime("%Y%m%d%H%M")
                add_document_arrival_auto_parts(callback.from_user.id, auto_part[0], invoice_date, data['message_data'][6], data['message_data'][4])
            await callback.message.answer('Успешно')
            delete_state()
            delete_state()
            await ModeratorStatesGroup.data.set()
            text, kb = keyboards.moderator.get_data_kb(data['action_datas'])
            await callback.message.answer(text=text,
                                          reply_markup=kb)


# Обработчик выбора действие с записью
@dp.callback_query_handler(CallbackData('subdata', 'id', 'action').filter(), state=ModeratorStatesGroup.subdata)
async def subdata(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2], action=data['action_datas'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'delete_subdata':
        async with state.proxy() as data:
            delete_subdata(data['action_datas'], callback_data['id'])
            await callback.answer('Запись успешно удалена!')
            text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2], action=data['action_datas'])
        await set_state()
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()


# Документы

# Обработчик выбора типа документов
@dp.callback_query_handler(CallbackData('documents_types', 'id', 'action').filter(), state=ModeratorStatesGroup.documents_types)
async def select_document_type(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    else:
        reset_main_page_entries()
        await ModeratorStatesGroup.documents.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['document_type_id'] = callback_data['id']
        text, kb = keyboards.moderator.get_documents_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик выбора документа
@dp.callback_query_handler(CallbackData('documents', 'id', 'action').filter(), state=ModeratorStatesGroup.documents)
async def select_document(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
    if callback_data['action'] == 'left_page' or callback_data['action'] == 'right_page':
        change_page(callback_data['action'])
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_documents_kb(data['document_type_id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
    if callback_data['action'] == 'document':
        await ModeratorStatesGroup.document.set()
        add_state(await state.get_state())
        text, kb = keyboards.moderator.get_document_kb(callback_data['id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)


# Обработчик возвращения из документа:
@dp.callback_query_handler(CallbackData('document', 'action').filter(), state=ModeratorStatesGroup.document)
async def back_document(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            text, kb = keyboards.moderator.get_keyboard(STATES_LIST[-2], document_type_id=data['document_type_id'])
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)
        delete_state()
