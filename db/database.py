# Файл класса базы данных

import psycopg2

from config.db import host, user, password, db_name


# Класс базы данных
class Database:

    # Инициализатор подключения и курсора
    def __init__(self):
        self.conn = None
        self.cur = None

    # Подключение к бд
    def connect(self):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name
        )
        self.cur = self.conn.cursor()

    # Закрытие подключения
    def close(self):
        self.cur.close()
        self.conn.close()

    # Создание таблиц
    def create_table(self, query):
        self.cur.execute(query)
        self.conn.commit()

    # Вернуть данные запроса
    def return_select_query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    # Выполнить запрос
    def execute_query(self, query):
        self.cur.execute(query)
        self.conn.commit()


# Обеькт базы данных
database_instance = Database()
# Подключение
database_instance.connect()
