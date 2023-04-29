# Файл создания таблиц базы данных

from db.database import database_instance


# Подключение к бд
database_instance.connect()


# Таблица пользователей
def users():
    query = '''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        fullname VARCHAR (100) NOT NULL,
        username VARCHAR (50) NOT NULL,
        phone INTEGER,
        email VARCHAR (100),
        role_id INTEGER DEFAULT 1,
        address_delivery VARCHAR (200),
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (role_id) REFERENCES roles (id)
    );'''
    database_instance.create_table(query=query)


# Таблица ролей
def roles():
    query = '''CREATE TABLE roles (
        id SERIAL PRIMARY KEY,
        role VARCHAR (100) NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE
    );'''
    database_instance.create_table(query=query)


# Таблица работников
def workers():
    query = '''CREATE TABLE workers (
        user_id INTEGER NOT NULL,
        role_id INTEGER NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (role_id) REFERENCES roles (id)
    );'''
    database_instance.create_table(query=query)


# Таблица марок авто
def cars_brands():
    query = '''CREATE TABLE cars_brands (
        id SERIAL PRIMARY KEY,
        name VARCHAR (100) NOT NULL,
        name_lc VARCHAR (100) NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE
    );'''
    database_instance.create_table(query=query)


# Таблица моделей авто
def cars_models():
    query = '''CREATE TABLE cars_models (
        id SERIAL PRIMARY KEY,
        car_brand_id INTEGER NOT NULL,
        name VARCHAR (100) NOT NULL,
        name_lc VARCHAR (100) NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (car_brand_id) REFERENCES cars_brands (id)
    );'''
    database_instance.create_table(query=query)


# Таблица подмоделей авто
def cars_submodels():
    query = '''CREATE TABLE cars_submodels (
        id SERIAL PRIMARY KEY,
        car_model_id INTEGER NOT NULL,
        name VARCHAR (100) NOT NULL,
        name_lc VARCHAR (100) NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (car_model_id) REFERENCES cars_models (id)
    );'''
    database_instance.create_table(query=query)


# Таблица модификаций авто
def cars_modifications():
    query = '''CREATE TABLE cars_modifications (
        id SERIAL PRIMARY KEY,
        car_submodel_id INTEGER NOT NULL,
        name_configuration VARCHAR NOT NULL,
        name_lc VARCHAR (100) NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (car_submodel_id) REFERENCES cars_submodels (id)
    );'''
    database_instance.create_table(query=query)


# Таблица категорий автозапчастей
def category_auto_parts():
    query = '''CREATE TABLE category_auto_parts (
        id SERIAL PRIMARY KEY,
        name VARCHAR (100) NOT NULL,
        name_lc VARCHAR (100) NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE
    );'''
    database_instance.create_table(query=query)


# Таблица подкатегорий автозапчастей
def subcategory_auto_parts():
    query = '''CREATE TABLE subcategory_auto_parts (
        id SERIAL PRIMARY KEY,
        category_id INTEGER NOT NULL,
        name VARCHAR (100) NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE,
        name_lc VARCHAR (100) NOT NULL,
        FOREIGN KEY (category_id) REFERENCES category_auto_parts (id)
    );'''
    database_instance.create_table(query=query)


# Таблица автозапчастей
def auto_parts():
    query = '''CREATE TABLE auto_parts (
        id SERIAL PRIMARY KEY,
        subcategory_id INTEGER NOT NULL,
        name VARCHAR (100) NOT NULL,
        brand VARCHAR (100),
        article VARCHAR (100),
        description VARCHAR,
        price INTEGER NOT NULL,
        photo VARCHAR,
        count INTEGER NOT NULL,
        name_lc VARCHAR (100) NOT NULL,
        suitable_for_models VARCHAR,
        car_model_id INTEGER,
        car_submodel_id INTEGER,
        car_modification_id INTEGER,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (subcategory_id) REFERENCES subcategory_auto_parts (id),
        FOREIGN KEY (car_model_id) REFERENCES cars_models (id),
        FOREIGN KEY (car_submodel_id) REFERENCES cars_submodels (id),
        FOREIGN KEY (car_modification_id) REFERENCES cars_modifications (id)
    );'''
    database_instance.create_table(query=query)


# Таблица подбора автозапчастей
def selection_auto_parts():
    query = '''CREATE TABLE selection_auto_parts (
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        name_lc VARCHAR NOT NULL,
        user_id INTEGER NOT NULL,
        car_brand_id INTEGER NOT NULL,
        car_model_id INTEGER NOT NULL,
        car_submodel_id INTEGER NOT NULL,
        car_modification_id INTEGER NOT NULL,
        viewing_status BOOLEAN DEFAULT FALSE,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (car_brand_id) REFERENCES cars_brands (id),
        FOREIGN KEY (car_model_id) REFERENCES cars_models (id),
        FOREIGN KEY (car_submodel_id) REFERENCES cars_submodels (id),
        FOREIGN KEY (car_modification_id) REFERENCES cars_modifications (id)
    );'''
    database_instance.create_table(query=query)


# Таблица корзины
def basket():
    query = '''CREATE TABLE basket (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        auto_part_id INTEGER NOT NULL,
        count INTEGER NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (auto_part_id) REFERENCES auto_parts (id)
    );'''
    database_instance.create_table(query=query)


# Таблица заказов
def orders():
    query = '''CREATE TABLE orders (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        reg_date BIGINT NOT NULL,
        is_paid BOOLEAN DEFAULT FALSE,
        is_delivered BOOLEAN DEFAULT FALSE,
        total_price INTEGER NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );'''
    database_instance.create_table(query=query)


# Таблица деталей заказов
def orders_items():
    query = '''CREATE TABLE orders_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        auto_part_id INTEGER NOT NULL,
        count INTEGER NOT NULL,
        price INTEGER NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (auto_part_id) REFERENCES auto_parts (id)
    );'''
    database_instance.create_table(query=query)


# Таблица доставки
def delivery():
    query = '''CREATE TABLE delivery (
        worker_id INTEGER,
        order_id INTEGER NOT NULL,
        is_completed BOOLEAN DEFAULT FALSE,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (worker_id) REFERENCES users (id),
        FOREIGN KEY (order_id) REFERENCES orders (id)
    );'''
    database_instance.create_table(query=query)


# Таблица типов документов
def documents_types():
    query = '''CREATE TABLE documents_types (
        id SERIAL PRIMARY KEY,
        name VARCHAR (100) NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE
    );'''
    database_instance.create_table(query=query)


# Таблица документов
def documents():
    query = '''CREATE TABLE documents (
        id SERIAL PRIMARY KEY,
        document_type_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        auto_part_id INTEGER NOT NULL,
        invoice_date BIGINT NOT NULL,
        count INTEGER NOT NULL,
        cost INTEGER NOT NULL,
        is_deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (document_type_id) REFERENCES documents_types (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (auto_part_id) REFERENCES auto_parts (id)
    );'''
    database_instance.create_table(query=query)


# Создание таблиц
def create_table():
    # roles()
    # users()
    # workers()

    # cars_brands()
    # cars_models()
    # cars_submodels()
    # cars_modifications()

    # category_auto_parts()
    # subcategory_auto_parts()
    # auto_parts()
    # selection_auto_parts()

    # basket()
    # orders()
    # orders_items()
    delivery()

    # documents_types()
    # documents()


# Вызов функции создания таблиц
create_table()


# Закрытие подключения к бд
database_instance.close()
