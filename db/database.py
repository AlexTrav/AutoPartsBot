# Файл класса базы данных
import logging

import psycopg2

from config.db import host, user, password, db_name


logger = logging.getLogger('app.db.database', )


# Класс базы данных
class Database:

    # Инициализатор подключения и курсора
    def __init__(self):
        self.conn = None
        self.cur = None

    # Подключение к бд
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                dbname=db_name
            )
            self.cur = self.conn.cursor()
            logger.info('Connection to the database is successful')
        except Exception as err:
            logger.error(f'An error has occurred: {err}')

    # Закрытие подключения
    def close(self):
        try:
            self.cur.close()
            self.conn.close()
            logger.info('Connection closed successfully')
        except Exception as err:
            logger.error(f'An error has occurred: {err}')

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

