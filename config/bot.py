# Файл получения токена бота

from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

BOT_TOKEN_API = getenv('BOT_TOKEN_API')
