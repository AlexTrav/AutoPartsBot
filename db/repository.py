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


# Manager


# Courier


