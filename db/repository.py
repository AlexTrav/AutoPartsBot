# Файл содержащий функции для взаимодействия с базой данных

from db.database import database_instance


# Users

# Проверка на существование пользователя в бд
def check_user(**kwargs):
    users = database_instance.return_select_query(query='SELECT * FROM users')
    if not users:
        database_instance.execute_query(query=f"INSERT INTO users(id, fullname, username) VALUES ({kwargs['user_id']}, '{kwargs['fullname']}', '{kwargs['username']}')")
    else:
        user = database_instance.return_select_query(query=f'SELECT * FROM users WHERE id = {kwargs["user_id"]}')
        if not user:
            database_instance.execute_query(query=f'INSERT INTO users(id, fullname, username) VALUES ({kwargs["user_id"]}, "{kwargs["fullname"]}", "{kwargs["username"]}")')


# Возвращает id роли
def get_role_id(**kwargs):
    role_id = database_instance.return_select_query(f'SELECT role_id FROM users WHERE id = {kwargs["user_id"]}')[0][0]
    return role_id


# Каталог автозапчастей

# Добавить автозапчасть в корзину
def add_basket_auto_part(**kwargs):
    answer = ''
    auto_part_count = database_instance.return_select_query(f'SELECT count FROM auto_parts WHERE id = {kwargs["auto_part_id"]}')[0][0]
    if kwargs['action'] == 'add_basket_count':
        database_instance.execute_query(f'INSERT INTO basket(user_id, auto_part_id, count) VALUES {kwargs["user_id"], kwargs["auto_part_id"], 1}')
        answer = 'Товар успешно добавлен в корзину!'
    if kwargs['action'] == 'inc_basket_count':
        if auto_part_count > database_instance.return_select_query(f'SELECT count FROM basket WHERE user_id = {kwargs["user_id"]} AND auto_part_id = {kwargs["auto_part_id"]}')[0][0]:
            database_instance.execute_query(f'UPDATE basket SET count = count + 1 WHERE user_id = {kwargs["user_id"]} AND auto_part_id = {kwargs["auto_part_id"]}')
            count = database_instance.return_select_query(f'SELECT count FROM basket WHERE user_id = {kwargs["user_id"]} AND auto_part_id = {kwargs["auto_part_id"]}')[0][0]
            answer = f'Товар + 1! Всего: {count}'
        else:
            answer = 'На складе столько нет!'
    if kwargs['action'] == 'dec_basket_count':
        if database_instance.return_select_query(f'SELECT count FROM basket WHERE user_id = {kwargs["user_id"]} AND auto_part_id = {kwargs["auto_part_id"]}')[0][0] == 1:
            database_instance.execute_query(f'DELETE FROM basket WHERE user_id = {kwargs["user_id"]} AND auto_part_id = {kwargs["auto_part_id"]}')
            answer = 'Товар успешно удалён из корзины!'
        else:
            database_instance.execute_query(f'UPDATE basket SET count = count - 1 WHERE user_id = {kwargs["user_id"]} AND auto_part_id = {kwargs["auto_part_id"]}')
            count = database_instance.return_select_query(f'SELECT count FROM basket WHERE user_id = {kwargs["user_id"]} AND auto_part_id = {kwargs["auto_part_id"]}')[0][0]
            answer = f'Товар - 1! Всего: {count}'
    return answer


# Подбор автозапчастей

# Добавить заявку на подбор автозапчастей
def add_selection_auto_parts(**kwargs):
    database_instance.execute_query(f"INSERT INTO selection_auto_parts(name, name_lc, user_id, car_brand_id, car_model_id, car_submodel_id, car_modification_id) VALUES ('{kwargs['name']}', '{kwargs['name'].lower()}', {kwargs['user_id']}, {kwargs['car_brand_id']}, {kwargs['car_model_id']}, {kwargs['car_submodel_id']}, {kwargs['car_modification_id']})")


# Корзина

# Очистить корзину
def delete_from_user_basket(user_id):
    database_instance.execute_query(f"DELETE FROM basket WHERE user_id = {user_id}")


# Редактирование корзины
def delete_from_user_basket_item(basket_id):
    database_instance.execute_query(f"DELETE FROM basket WHERE id = {basket_id}")


# Оформление заказа
def place_in_order(user_id, reg_date, total_price):
    database_instance.execute_query(f"INSERT INTO orders(user_id, reg_date, total_price) VALUES ({user_id}, {reg_date}, {total_price})")
    order_id = database_instance.return_select_query(f"SELECT id FROM orders WHERE reg_date = {reg_date}")[0][0]
    return order_id


def place_in_order_item(order_id, user_id, auto_part_id, count, price):
    database_instance.execute_query(f"INSERT INTO orders_items(order_id, user_id, auto_part_id, count, price) VALUES ({order_id}, {user_id}, {auto_part_id}, {count}, {price})")


# Заказы


# Поиск


# Профиль


# О нас


# Manager


# Courier


