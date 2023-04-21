# Файл обработчик команды start

from aiogram import types

from bot.loader import dp

from bot.states import UserStatesGroup, ManagerStatesGroup, CourierStatesGroup

from bot.keyboards import user_keyboards, manager_keyboards, courier_keyboards
from db import repository


# Обработчик команды start
@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message):
    repository.check_user(user_id=message.from_user.id, fullname=message.from_user.first_name + ' ' + message.from_user.last_name, username=message.from_user.username)
    status_id = repository.get_role_id(user_id=message.from_user.id)
    if status_id == 1:
        await UserStatesGroup.start.set()
        text, kb = user_keyboards.get_start_kb()
        await message.answer(text=text,
                             reply_markup=kb)
    elif status_id == 2:
        await ManagerStatesGroup.start.set()
        text, kb = manager_keyboards.get_start_kb()
        await message.answer(text=text,
                             reply_markup=kb)
    elif status_id == 3:
        await CourierStatesGroup.start.set()
        text, kb = courier_keyboards.get_start_kb()
        await message.answer(text=text,
                             reply_markup=kb)
