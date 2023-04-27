# Файл обработчик команды start

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.loader import dp

from bot.states import UserStatesGroup, ModeratorStatesGroup, CourierStatesGroup

from bot.keyboards import user, moderator, courier
from bot.keyboards.back_button import *

from db import repository


# Обработчик команды start
@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message, state: FSMContext):
    delete_all_states()
    repository.check_user(user_id=message.from_user.id, fullname=message.from_user.first_name + ' ' + message.from_user.last_name, username=message.from_user.username)
    status_id = repository.get_role_id(user_id=message.from_user.id)
    if status_id == 1:
        await UserStatesGroup.start.set()
        add_state(await state.get_state())
        text, kb = user.get_start_kb(message.from_user.id)
        await message.answer(text=text,
                             reply_markup=kb)
    elif status_id == 2:
        await ModeratorStatesGroup.start.set()
        add_state(await state.get_state())
        text, kb = moderator.get_start_kb()
        await message.answer(text=text,
                             reply_markup=kb)
    elif status_id == 3:
        await CourierStatesGroup.start.set()
        add_state(await state.get_state())
        text, kb = courier.get_start_kb()
        await message.answer(text=text,
                             reply_markup=kb)
