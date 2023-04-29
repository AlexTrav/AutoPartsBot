# Файл отправки клавиатур и сообщений модератора

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.keyboards import MainPage, add_pagination_to_kb
from db.database import database_instance


# Отправить клавиатуру в зависимости от состояния
def get_keyboard(state, **kwargs):
    if state == 'ModeratorStatesGroup:start':
        return get_start_kb()

    if state == 'ModeratorStatesGroup:selection_auto_parts':
        return get_selection_auto_parts_kb()

    if state == 'ModeratorStatesGroup:users':
        return get_users_kb()
    if state == 'ModeratorStatesGroup:add_balance_select_user':
        return get_add_balance_select_user_kb()
    if state == 'ModeratorStatesGroup:set_roles_select_user':
        return get_set_roles_select_user_kb()

    if state == 'ModeratorStatesGroup:datas':
        return get_datas_kb()
    if state == 'ModeratorStatesGroup:data':
        return get_data_kb(kwargs['action'])
    if state == 'ModeratorStatesGroup:add_data':
        return get_add_data_kb(kwargs['action'])

    if state == 'ModeratorStatesGroup:documents_types':
        return get_documents_types_kb()
    if state == 'ModeratorStatesGroup:documents':
        return get_documents_kb(kwargs['document_type_id'])


# Клавиатура команды start
def get_start_kb():
    text = 'Модератор добро пожаловать в Auto-Parts Bot!'
    cb = CallbackData('main_menu', 'action')
    start_moderator_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подбор автозапчастей', callback_data=cb.new(action='selection_auto_parts'))],
        [InlineKeyboardButton(text='Пользователи', callback_data=cb.new(action='users'))],
        [InlineKeyboardButton(text='Данные', callback_data=cb.new(action='datas'))],
        [InlineKeyboardButton(text='Документы', callback_data=cb.new(action='documents'))],
        [InlineKeyboardButton(text='Выйти', callback_data=cb.new(action='exit'))]
    ])
    return text, start_moderator_kb


# Подбор автозапчастей

# Клавиатура выбора заявки на подбор автозапчастей
def get_selection_auto_parts_kb():
    cb = CallbackData('selection_auto_parts', 'id', 'action')
    text = 'Обработка заявок на подбор автозапчастей\nВыберите заявку:'
    selection_auto_parts_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query("SELECT * FROM selection_auto_parts")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            selection_auto_parts_kb.add(
                InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='application')))
        selection_auto_parts_kb = add_pagination_to_kb(kb=selection_auto_parts_kb, cb=cb, len_data=len(entries),
                                                       id_btn=0)
    else:
        for entry in entries:
            selection_auto_parts_kb.add(
                InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='application')))
    selection_auto_parts_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, selection_auto_parts_kb


# Клавиатура заявки на подбор автозапчастей
def get_application_kb(application_id):
    cb = CallbackData('application', 'action')
    application_kb = InlineKeyboardMarkup()
    application = database_instance.return_select_query(f"SELECT * FROM selection_auto_parts WHERE id = {application_id}")[0]
    if application[8] is False:
        database_instance.execute_query(f"UPDATE selection_auto_parts SET viewing_status = true")
    user_application = database_instance.return_select_query(f"SELECT * FROM users WHERE id = {application[3]}")[0]
    car_brand = database_instance.return_select_query(f"SELECT * FROM cars_brands WHERE id = {application[4]}")[0]
    car_model = database_instance.return_select_query(f"SELECT * FROM cars_models WHERE id = {application[5]}")[0]
    car_submodel = database_instance.return_select_query(f"SELECT * FROM cars_submodels WHERE id = {application[6]}")[0]
    car_modification = database_instance.return_select_query(f"SELECT * FROM cars_modifications WHERE id = {application[7]}")[0]
    viewing_status = 'Просмотрен' if application[8] else 'Не просмотрен'
    text = f'Заявка под номером: {application[0]}\n\nПользователь: \nЗаявка подана пользователем под именем: {user_application[1]}\n\nДетали заявки:\nНаименование автозапчасти/автозапчастей: {application[1]}\nБрэнд авто: {car_brand[1]}\nМодель авто: {car_model[2]}\nКонфигурация авто: {car_submodel[2]}\nМодификация авто: {car_modification[2]}\nСтатус просмотра: {viewing_status}'
    url = f'https://t.me/{user_application[2]}'
    application_kb.add(InlineKeyboardButton(text=user_application[1], url=url))
    application_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, application_kb


# Пользователи

# Клавиатура работы с пользователями
def get_users_kb():
    cb = CallbackData('users', 'action')
    text = 'Работа с пользователем\nВыберите действие:'
    users_kb = InlineKeyboardMarkup()
    users_kb.add(InlineKeyboardButton(text='Пополнение баланса пользователя', callback_data=cb.new(action='add_balance_select_user')))
    users_kb.add(InlineKeyboardButton(text='Выдача ролей пользователю', callback_data=cb.new(action='set_roles_select_user')))
    users_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, users_kb


# Клавиатура выбора пользователя для пополнения баланса
def get_add_balance_select_user_kb():
    cb = CallbackData('add_balance_select_user', 'id', 'action')
    text = 'Выберите пользователя для пополнения баланса:'
    select_user_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query("SELECT * FROM users")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            select_user_kb.add(InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='user')))
        select_user_kb = add_pagination_to_kb(kb=select_user_kb, cb=cb, len_data=len(entries), id_btn=0)
    else:
        for entry in entries:
            select_user_kb.add(InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='user')))
    select_user_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, select_user_kb


# Клавиатура выбора пользователя для выдачи ролей
def get_set_roles_select_user_kb():
    cb = CallbackData('set_roles_select_user', 'id', 'action')
    text = 'Выберите пользователя для выдачи ролей:'
    select_user_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query("SELECT * FROM users")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            select_user_kb.add(InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='user')))
        select_user_kb = add_pagination_to_kb(kb=select_user_kb, cb=cb, len_data=len(entries), id_btn=0)
    else:
        for entry in entries:
            select_user_kb.add(InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='user')))
    select_user_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, select_user_kb


# Клавиатура пополнения баланса
def get_add_balance_kb(user_id):
    cb = CallbackData('add_balance', 'action')
    user = database_instance.return_select_query(f"SELECT * FROM users WHERE id = {user_id}")[0]
    text = f'Введите сумму, на которую хотите пополнить баланс, пользователю под именем: {user[1]}'
    add_balance_kb = InlineKeyboardMarkup()
    url = f'https://t.me/{user[2]}'
    add_balance_kb.add(InlineKeyboardButton(text=user[1], url=url))
    add_balance_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, add_balance_kb


# Клавиатура выдачи ролей
def get_set_roles_kb(user_id):
    cb = CallbackData('set_roles', 'action')
    user = database_instance.return_select_query(f"SELECT * FROM users WHERE id = {user_id}")[0]
    text = f'Пользователь: {user[1]}\n'
    set_roles_kb = InlineKeyboardMarkup()
    if database_instance.return_select_query(f"SELECT * FROM workers WHERE user_id = {user_id} and role_id = 2"):
        text += 'Владеет ролью: <<Модератор>>\n'
        set_roles_kb.add(InlineKeyboardButton(text='Убрать роль модератора', callback_data=cb.new(action='delete_role_moderator')))
    else:
        set_roles_kb.add(InlineKeyboardButton(text='Добавить роль модератора', callback_data=cb.new(action='add_role_moderator')))
    if database_instance.return_select_query(f"SELECT * FROM workers WHERE user_id = {user_id} and role_id = 3"):
        text += 'Владеет ролью: <<Курьер>>\n'
        set_roles_kb.add(InlineKeyboardButton(text='Убрать роль курьера', callback_data=cb.new(action='delete_role_courier')))
    else:
        set_roles_kb.add(InlineKeyboardButton(text='Добавить роль курьера', callback_data=cb.new(action='add_role_courier')))
    url = f'https://t.me/{user[2]}'
    set_roles_kb.add(InlineKeyboardButton(text=user[1], url=url))
    set_roles_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, set_roles_kb


# Данные

# Клавиатура работы с данными
def get_datas_kb():
    cb = CallbackData('datas', 'action')
    text = 'Выберите таблицу данных:'
    datas_kb = InlineKeyboardMarkup()
    datas_kb.add(InlineKeyboardButton(text='Категория автозапчастей', callback_data=cb.new(action='category_auto_parts')))
    datas_kb.add(InlineKeyboardButton(text='Подкатегория автозапчастей', callback_data=cb.new(action='subcategory_auto_parts')))
    datas_kb.add(InlineKeyboardButton(text='Автозапчасти', callback_data=cb.new(action='auto_parts')))
    datas_kb.add(InlineKeyboardButton(text='Бренды авто', callback_data=cb.new(action='cars_brands')))
    datas_kb.add(InlineKeyboardButton(text='Модели авто', callback_data=cb.new(action='cars_models')))
    datas_kb.add(InlineKeyboardButton(text='Конфигурации авто', callback_data=cb.new(action='cars_submodels')))
    datas_kb.add(InlineKeyboardButton(text='Модификации авто', callback_data=cb.new(action='cars_modifications')))
    datas_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, datas_kb


# Клавиатура выбора данных
def get_data_kb(action):
    cb = CallbackData('data', 'id', 'action')
    text = 'Выберите запись или действие:'
    data_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query(f"SELECT * FROM {action} WHERE is_deleted = false")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            if action == 'category_auto_parts' or action == 'cars_brands':
                data_kb.add(InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='subdata')))
            else:
                data_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='subdata')))
        data_kb = add_pagination_to_kb(kb=data_kb, cb=cb, len_data=len(entries), id_btn=0)
    else:
        for entry in entries:
            if action == 'category_auto_parts' or action == 'cars_brands':
                data_kb.add(InlineKeyboardButton(text=entry[1], callback_data=cb.new(id=entry[0], action='subdata')))
            else:
                data_kb.add(InlineKeyboardButton(text=entry[2], callback_data=cb.new(id=entry[0], action='subdata')))
    data_kb.add(InlineKeyboardButton(text='Добавить запись', callback_data=cb.new(id=-2, action='add_data')))
    data_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, data_kb


# Клавиатура добавление данных
def get_add_data_kb(action):
    cb = CallbackData('add_data', 'action')
    add_data_kb = InlineKeyboardMarkup()
    text = ''
    if action == 'category_auto_parts':
        text = 'Добавление категории автозапчастей\nВведите наименование категории:'
    if action == 'subcategory_auto_parts':
        text = 'Добавление подкатегории автозапчастей\nВведите наименование подкатегории:'
    if action == 'auto_parts':
        text = 'Добавление автозапчасти\nВведите наименование, производителя, артикул, описание, цену, фото и количество автозапчасти:\nКаждое поле с новой строки!'
    if action == 'cars_brands':
        text = 'Добавление брэнда авто:\nВведите наименование брэнда авто:'
    if action == 'cars_models':
        text = 'Добавление модели авто:\nВведите наименование модели авто:'
    if action == 'cars_submodels':
        text = 'Добавление конфигурации авто:\nВведите наименование конфигурации авто:'
    if action == 'cars_modifications':
        text = 'Добавление модификации авто:\nВведите наименование модификации авто:'
    add_data_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, add_data_kb


# Клавиатура выбора ключа для добавления данных
def get_set_key_for_add_data_kb(action):
    subaction = ''
    if action == 'subcategory_auto_parts':
        subaction = 'category_auto_parts'
    if action == 'auto_parts':
        subaction = 'subcategory_auto_parts'
    if action == 'cars_models':
        subaction = 'cars_brands'
    if action == 'cars_submodels':
        subaction = 'cars_models'
    if action == 'cars_modifications':
        subaction = 'cars_submodels'
    cb = CallbackData('set_key_for_add_data', 'id', 'action')
    text = 'Выберите ключ:'
    data_key_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query(f"SELECT * FROM {subaction} WHERE is_deleted = false")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            if subaction == 'category_auto_parts' or subaction == 'cars_brands':
                data_key_kb.add(InlineKeyboardButton(text=f'{entry[0]}:{entry[1]}', callback_data=cb.new(id=entry[0], action='key')))
            else:
                data_key_kb.add(InlineKeyboardButton(text=f'{entry[0]}:{entry[2]}', callback_data=cb.new(id=entry[0], action='key')))
        data_key_kb = add_pagination_to_kb(kb=data_key_kb, cb=cb, len_data=len(entries), id_btn=0)
    else:
        for entry in entries:
            if subaction == 'category_auto_parts' or subaction == 'cars_brands':
                data_key_kb.add(InlineKeyboardButton(text=f'{entry[0]}:{entry[1]}', callback_data=cb.new(id=entry[0], action='key')))
            else:
                data_key_kb.add(InlineKeyboardButton(text=f'{entry[0]}:{entry[2]}', callback_data=cb.new(id=entry[0], action='key')))
    data_key_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, data_key_kb


# Клавитура записи данных
def get_subdata_kb(action, subdata_id):
    cb = CallbackData('subdata', 'id', 'action')
    subdata_kb = InlineKeyboardMarkup()
    subdata = database_instance.return_select_query(f"SELECT * FROM {action} WHERE id = {subdata_id}")[0]
    text = ''
    if action == 'category_auto_parts':
        text = f'Категория автозапчастей:\nКлюч: {subdata[0]}\nНаименование: {subdata[1]}'
    if action == 'subcategory_auto_parts':
        text = f'Подкатегория автозапчастей:\nКлюч: {subdata[0]}\nКлюч категории: {subdata[1]}\nНаименование: {subdata[2]}'
    if action == 'auto_parts':
        text = f'Автозапчасть:\nКлюч: {subdata[0]}\nКлюч подкатегории: {subdata[1]}\nНаименование: {subdata[2]}\nПроизводитель: {subdata[3]}\nАртикул: {subdata[4]}\nОписание: {subdata[5]}\nЦена: {subdata[6]}\nФото: {subdata[7]}\nКоличество на складу: {subdata[8]}'
    if action == 'cars_brands':
        text = f'Брэнд авто:\nКлюч: {subdata[0]}\nНаименование: {subdata[1]}'
    if action == 'cars_models':
        text = f'Модель авто:\nКлюч: {subdata[0]}\nКлюч бренда авто: {subdata[1]}\nНаименование: {subdata[2]}'
    if action == 'cars_submodels':
        text = f'Конфигурация авто:\nКлюч: {subdata[0]}\nКлюч модели авто: {subdata[1]}\nНаименование: {subdata[2]}'
    if action == 'cars_modifications':
        text = f'Модификация авто:\nКлюч: {subdata[0]}\nКлюч конфигурации авто: {subdata[1]}\nНаименование: {subdata[2]}'
    subdata_kb.add(InlineKeyboardButton(text='Удалить запись', callback_data=cb.new(id=subdata_id, action='delete_subdata')))
    subdata_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, subdata_kb


# Документы

# Клавиатура выбора типа документов
def get_documents_types_kb():
    cb = CallbackData('documents_types', 'id', 'action')
    text = 'Выберите тип документов:'
    documents_types_kb = InlineKeyboardMarkup()
    documents_types_kb.add(InlineKeyboardButton(text='Прибытие автозапчастей', callback_data=cb.new(id=1, action='arrival_auto_parts')))
    documents_types_kb.add(InlineKeyboardButton(text='Убытие автозапчастей', callback_data=cb.new(id=2, action='departure_auto_parts')))
    documents_types_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, documents_types_kb


# Клавиатура работы с документами
def get_documents_kb(document_type_id):
    cb = CallbackData('documents', 'id', 'action')
    text = 'Выберите документ:'
    documents_kb = InlineKeyboardMarkup()
    entries = database_instance.return_select_query(f"SELECT * FROM documents WHERE document_type_id = {document_type_id}")
    if len(entries) > 10:
        for entry in entries[MainPage.entries - 10:MainPage.entries]:
            reg_date = str(entry[4])[6:8] + '.' + str(entry[4])[4:6] + '.' + str(entry[4])[2:4] + ' ' + str(entry[4])[8:10] + ':' + str(entry[4])[10:]
            documents_kb.add(InlineKeyboardButton(text=reg_date, callback_data=cb.new(id=entry[0], action='document')))
        documents_kb = add_pagination_to_kb(kb=documents_kb, cb=cb, len_data=len(entries), id_btn=0)
    else:
        for entry in entries:
            reg_date = str(entry[4])[6:8] + '.' + str(entry[4])[4:6] + '.' + str(entry[4])[2:4] + ' ' + str(entry[4])[8:10] + ':' + str(entry[4])[10:]
            documents_kb.add(InlineKeyboardButton(text=reg_date, callback_data=cb.new(id=entry[0], action='document')))
    documents_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(id=-1, action='back')))
    return text, documents_kb


# Клавиатура документа
def get_document_kb(document_id):
    cb = CallbackData('document', 'action')
    document = database_instance.return_select_query(f"SELECT * FROM documents WHERE id = {document_id}")[0]
    type_document = 'Прибытие товара' if document[1] == 1 else 'Убытие товара'
    user = database_instance.return_select_query(f"SELECT * FROM users WHERE id = {document[2]}")[0]
    url = f'https://t.me/{user[2]}'
    auto_part = database_instance.return_select_query(f"SELECT * FROM auto_parts WHERE id = {document[3]}")[0]
    reg_data = str(document[4])[6:8] + '.' + str(document[4])[4:6] + '.' + str(document[4])[2:4] + ' ' + str(document[4])[8:10] + ':' + str(document[4])[10:]
    text = f"Документ: {document[0]}\nТип документа: {type_document}\nВыполненно пользователем: {user[1]}\nСсылка на пользователя: {url}\nАвтозапчасть: {auto_part[2]}\nДата добавления документа: {reg_data}\nКоличество: {document[5]}\nЦена: {document[6]}"
    document_kb = InlineKeyboardMarkup()
    document_kb.add(InlineKeyboardButton(text='<<', callback_data=cb.new(action='back')))
    return text, document_kb
