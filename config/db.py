# Файл получения переменных подключения


from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


host = getenv('HOST')
user = getenv('USER')
password = getenv('PASSWORD')
db_name = getenv('DB_NAME')
