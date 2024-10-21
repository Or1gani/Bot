import asyncio

from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline import get_callback_buttons, add_employee_callback, get_nick_confirm_btns, get_name1_confirm_btns
from keyboards.reply import get_buttons
from utils.menu_processing import get_setting_content
from assets.menu_data import desciption_for_pages_settings as dfps

from utils.FSMs import add_employee_states
from aiogram.fsm.context import FSMContext

admin_router = Router()

@admin_router.callback_query(F.data == 'add_employee')
async def set_role(callback: CallbackQuery):
    rm, text = get_setting_content(level=0, menu_name="role", data_for_db=None)
    await callback.message.edit_text(text=text, reply_markup=rm)

@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "nick"))
async def nick_telegram(callback: CallbackQuery, callback_data: add_employee_callback, state : FSMContext):
    print(callback_data.data_for_db)
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

@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "name1"))
async def name1(callback: CallbackQuery, callback_data: add_employee_callback, state : FSMContext):
    await state.clear()
    await state.set_state(add_employee_states.waiting_for_name1)
    rm, text = get_setting_content(level=callback_data.level, menu_name=callback_data.menu_name, data_for_db=callback_data.data_for_db)
    await callback.message.edit_text(text=text)



@admin_router.message(add_employee_states.waiting_for_name1)
async def process_name1(message: Message, state : FSMContext):
    name1 = message.text
    rm = get_name1_confirm_btns(level=2, data_for_db=name1)
    await message.answer(f"Вы уверены?", reply_markup=rm)

@admin_router.callback_query(add_employee_callback.filter(F.menu_name == "name2"))
async def name2(callback: CallbackQuery, callback_data: add_employee_callback, state : FSMContext):
    await state.clear()
    await state.set_state(add_employee_states.waiting_for_name2)
    rm, text = get_setting_content(level=callback_data.level, menu_name=callback_data.menu_name, data_for_db=callback_data.data_for_db)
    await callback.message.edit_text(text=text)