import asyncio

from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline import (get_callback_buttons, add_employee_callback, edit_employee_callback, get_nick_confirm_btns,
                              get_name1_confirm_btns, get_name2_confirm_btns, get_name3_confirm_btns, get_pass_btns, get_decide)
from keyboards.reply import get_buttons
from utils.menu_processing import get_setting_content
from assets.menu_data import desciption_for_pages_settings as dfps

from utils.FSMs import add_employee_states, edit_employee
from aiogram.fsm.context import FSMContext
from utils.db_data import create_or_update_data_for_sys, transfer_data, get_tg_name

from pyrogram import Client
from important_data.config import TOKEN, API_ID, API_HASH# параметры подключения к бд

admin_router = Router()
data = []
app = Client("my_bot", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH)

@admin_router.callback_query(F.data == "add_employee")
async def set_role(callback: CallbackQuery):
    rm, text = get_setting_content(level=0, menu_name="role", data_for_db=None)
    await callback.message.edit_text(text=text, reply_markup=rm)


@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "nick"))
async def nick_telegram(callback: CallbackQuery, callback_data: add_employee_callback, state : FSMContext):
    if callback_data.data_for_db == 'admin' or callback_data.data_for_db == 'courier':
        create_or_update_data_for_sys(callback_data.data_for_db, 'role', callback.from_user.id)
        data.append(callback_data.data_for_db)
    rm, text = get_setting_content(level=callback_data.level, menu_name=callback_data.menu_name, data_for_db=callback_data.data_for_db)
    await callback.message.edit_text(text=text)
    # Переход в состояние ожидания ввода имени
    await state.set_state(add_employee_states.waiting_for_nick)


@admin_router.message(add_employee_states.waiting_for_nick)
async def process_nick(message: Message, state : FSMContext):
    nick = message.text
    if (nick[0] == "@") and (" " not in nick):
        await state.clear()
        rm = get_nick_confirm_btns(level=1, data_for_db=nick)
        await message.answer(f"Вы уверены?", reply_markup=rm)
    else:
        await message.answer("Ник пользователя должен начинаться с '@' и не содержать пробелов!")
        await state.set_state(add_employee_states.waiting_for_nick)

async def get_user_id(username: str) -> int:
    if username.startswith('@'):
        try:
            user = await app.get_users(username)
            return user.id
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return None
    else:
        print("Юзернейм должен начинаться с '@'.")
        return None
@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "name1"))
async def name1(callback: CallbackQuery, callback_data: add_employee_callback, state : FSMContext):
    if callback_data.yes != None:
        if int(callback_data.yes) == 1:
            create_or_update_data_for_sys(callback_data.data_for_db, 'nick', callback.from_user.id)
            data.append(callback_data.data_for_db)

            user_id = await get_user_id(get_tg_name(callback.from_user.id))
            if user_id is not None:
                print(user_id)
                create_or_update_data_for_sys(user_id, "employee_tg_id", callback.from_user.id)
            else:
                print("Не удалось получить ID пользователя.")
                await callback.message.answer("Ник пользователя не существует!")
                await state.set_state(add_employee_states.waiting_for_nick)
                return
    await state.clear()
    await state.set_state(add_employee_states.waiting_for_name1)
    print(callback_data.data_for_db)
    rm, text = get_setting_content(level=callback_data.level, menu_name=callback_data.menu_name, data_for_db=callback_data.data_for_db)
    await callback.message.edit_text(text=text)


@admin_router.message(add_employee_states.waiting_for_name1)
async def process_name1(message: Message):
    name1 = message.text
    rm = get_name1_confirm_btns(level=2, data_for_db=name1)
    await message.answer(f"Вы уверены?", reply_markup=rm)


@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "name2"))
async def name2(callback: CallbackQuery, callback_data: add_employee_callback, state : FSMContext):
    if callback_data.yes != None:
        if int(callback_data.yes) == 1:
            create_or_update_data_for_sys(callback_data.data_for_db, 'name1', callback.from_user.id)
            data.append(callback_data.data_for_db)
    await state.clear()
    await state.set_state(add_employee_states.waiting_for_name2)
    print(callback_data.data_for_db)
    rm, text = get_setting_content(level=callback_data.level, menu_name=callback_data.menu_name, data_for_db=callback_data.data_for_db)
    await callback.message.edit_text(text=text)


@admin_router.message(add_employee_states.waiting_for_name2)
async def process_name2(message: Message):
    name2 = message.text
    rm = get_name2_confirm_btns(level=3, data_for_db=name2)
    await message.answer(f"Вы уверены?", reply_markup=rm)


@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "name3"))
async def name3(callback: CallbackQuery, callback_data: add_employee_callback, state : FSMContext):
    if callback_data.yes != None:
        if int(callback_data.yes) == 1:
            create_or_update_data_for_sys(callback_data.data_for_db, 'name2', callback.from_user.id)
            data.append(callback_data.data_for_db)
    await state.clear()
    await state.set_state(add_employee_states.waiting_for_name3)
    print(callback_data.data_for_db)
    rm, text = get_setting_content(level=callback_data.level, menu_name=callback_data.menu_name, data_for_db=callback_data.data_for_db)
    await callback.message.edit_text(text=text)


@admin_router.message(add_employee_states.waiting_for_name3)
async def process_name3(message: Message):
    name3 = message.text
    rm = get_name3_confirm_btns(level=4, data_for_db=name3)
    await message.answer(f"Вы уверены?", reply_markup=rm)


@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "pass"))
async def pas(callback: CallbackQuery, callback_data: add_employee_callback, state : FSMContext):
    if callback_data.yes != None:
        if int(callback_data.yes) == 1:
            create_or_update_data_for_sys(callback_data.data_for_db, 'name3', callback.from_user.id)
            data.append(callback_data.data_for_db)
    await state.clear()
    await state.set_state(add_employee_states.waiting_for_pass)
    print(callback_data.data_for_db)
    rm, text = get_setting_content(level=callback_data.level, menu_name=callback_data.menu_name, data_for_db=callback_data.data_for_db)
    await callback.message.edit_text(text=text)


@admin_router.message(add_employee_states.waiting_for_pass)
async def process_pass(message: Message):
    pas = message.text
    rm = get_pass_btns(level=5, data_for_db=pas)
    await message.answer(f"Вы уверены?", reply_markup=rm)


@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "correction"))
async def pas(callback: CallbackQuery, callback_data: add_employee_callback, state : FSMContext):
    create_or_update_data_for_sys(int(callback_data.data_for_db), 'region', callback.from_user.id)
    if callback_data.yes != None:
        if int(callback_data.yes) == 1:
            create_or_update_data_for_sys(callback_data.data_for_db, 'pass', callback.from_user.id)
            data.append(callback_data.data_for_db)
    await state.clear()
    rm, text = get_setting_content(level=callback_data.level, menu_name=callback_data.menu_name, data_for_db=callback_data.data_for_db)
    await callback.message.edit_text(text=text, reply_markup=rm)



@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "confirm_data"))
async def res(callback :  CallbackQuery):
    transfer_data()
    await callback.message.edit_text(f"Данные перенесены")


@admin_router.callback_query(edit_employee_callback.filter(F.take == '1'))
async def decide(callback: CallbackQuery, callback_data: edit_employee_callback, state: FSMContext):

    await state.update_data(menu_name=callback_data.menu_name)

    if callback_data.menu_name == "role":
        await state.set_state(edit_employee.waiting_for_data)
        await callback.message.edit_text(f"Введите роль сотрудника: ")
    elif callback_data.menu_name == "nick":
        await state.set_state(edit_employee.waiting_for_data)
        await callback.message.edit_text(f"Введите ник телеграм сотрудника: ")
    elif callback_data.menu_name == "name1":
        await state.set_state(edit_employee.waiting_for_data)
        await callback.message.edit_text(f"Введите Имя сотрудника: ")
    elif callback_data.menu_name == "name2":
        await state.set_state(edit_employee.waiting_for_data)
        await callback.message.edit_text(f"Введите Фамилию сотрудника: ")
    elif callback_data.menu_name == "name3":
        await state.set_state(edit_employee.waiting_for_data)
        await callback.message.edit_text(f"Введите Отчество сотрудника: ")
    elif callback_data.menu_name == "pass":
        await state.set_state(edit_employee.waiting_for_data)
        await callback.message.edit_text(f"Введите паспортные данные сотрудника: ")
    elif callback_data.menu_name == "region":
        rm, text = get_setting_content(level=callback_data.level, menu_name=callback_data.menu_name,
                                       data_for_db=callback_data.data_for_db)
        await callback.message.edit_text(text=text, reply_markup=rm)


@admin_router.message(edit_employee.waiting_for_data)
async def process_edit(message: Message, state: FSMContext):
    data = await state.get_data()
    menu_name: str = data.get('menu_name')
    rm = get_decide(menu_name=menu_name, value=message.text)
    await message.answer("Вы уверены?", reply_markup=rm)


@admin_router.callback_query(edit_employee_callback.filter(F.decide == 'True'))
async def ediit(callback: CallbackQuery, callback_data: edit_employee_callback, state: FSMContext):
    create_or_update_data_for_sys(callback_data.value, callback_data.menu_name, callback.from_user.id)
    await callback.message.edit_text(f"Данные сохранены со значением: {callback_data.value}")
    rm, text = get_setting_content(level=7, menu_name="correction",
                                   data_for_db=callback_data.value)
    await callback.message.edit_text(text=text, reply_markup=rm)
    await state.clear()


@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "region"))
async def nick_telegram(callback: CallbackQuery, callback_data: add_employee_callback):
    data.append(callback_data.data_for_db)
    create_or_update_data_for_sys(callback_data.data_for_db, 'pass', callback.from_user.id)
    rm, text = get_setting_content(level=callback_data.level, menu_name=callback_data.menu_name, data_for_db=callback_data.data_for_db)
    await callback.message.edit_text(text=text, reply_markup=rm)
