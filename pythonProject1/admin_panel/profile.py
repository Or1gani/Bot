from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline import get_callback_buttons, get_region_buttons, get_profile_button, \
    region_callback, name_callback, get_name_emplyees_buttons, get_back_to_panel, get_ticket_btns, ticket_callback
from utils.menu_processing import get_menu_content, get_ticket_content
from utils.db_data import (set_update_courier_amount, admin_valid, get_admin_panel_data, get_employees, reg_id_to_str,
                           regionid_to_regionname, update_region, get_name_by_tg_id, remove_ticket)

admin_profile_router = Router()

@admin_profile_router.message(Command('admin_panel'))
async def profile(message : Message):
    t_id = int(message.from_user.id)
    if admin_valid(t_id):
        controled_region, couriers_amount = get_admin_panel_data(t_id)
        rm = get_callback_buttons(buttons={'Список сотрудников':'employee_list', 'Запросы на смену района':'change_reg'}, sizes=(1,))
        await message.answer(text=f'Ваш регион: {controled_region}\nКоличество курьеров на районе: {couriers_amount}', reply_markup=rm)
    else:
        await message.answer(text='Не достаточно прав, обратитесь к администратору')

#запросы на смену района->
@admin_profile_router.callback_query(F.data == 'change_reg')
async def change_region(callback: CallbackQuery):
    rm = get_ticket_content(level=0, tg_id=None, fr=None, to=None)
    await callback.message.edit_text("Тикеты на смену района: ", reply_markup=rm)


@admin_profile_router.callback_query(ticket_callback.filter(F.level == 1))
async def display_tickets(callback: CallbackQuery, callback_data: ticket_callback):
    print(callback_data.level, callback_data.fr, callback_data.to)
    from_reg = regionid_to_regionname(callback_data.fr)
    to_reg = regionid_to_regionname(callback_data.to)
    name = get_name_by_tg_id(callback_data.tg_id)
    rm = get_ticket_content(level=callback_data.level, tg_id=callback_data.tg_id, fr=callback_data.fr, to=callback_data.to)
    await callback.message.edit_text(f"{name} - Хочет сменить район:\n{from_reg} -> {to_reg}", reply_markup=rm)


@admin_profile_router.callback_query(ticket_callback.filter(F.decide == "Yes"))
async def approve_ticket(callback: CallbackQuery, callback_data: ticket_callback):
    print("!!!", callback_data.tg_id, callback_data.fr, callback_data.to)
    update_region(callback_data.tg_id, callback_data.to)
    remove_ticket(callback_data.tg_id)
    await callback.answer("Тикет решен",cache_time=5)

    await bot.send_message(chat_id=callback_data.tg_id, text="Вам одобрена смена района")

    rm = get_ticket_content(level=0, tg_id=None, fr=None, to=None)
    await callback.message.edit_text("Тикеты на смену района: ", reply_markup=rm)


@admin_profile_router.callback_query(F.data == 'employee_list')
async def employee_list(callback : CallbackQuery):
    names, other_data = get_employees()
    rm = get_name_emplyees_buttons(names)
    await callback.message.edit_text(text="Сотрудники", reply_markup=rm)

@admin_profile_router.callback_query(F.data == 'back-to-admin-panel')
async def back_to_panel(callback: CallbackQuery):
    t_id = int(callback.from_user.id)
    if admin_valid(t_id):
        controled_region, couriers_amount = get_admin_panel_data(t_id)
        rm = get_callback_buttons(
            buttons={'Список сотрудников': 'employee_list', 'Запросы на смену района': 'change_reg'}, sizes=(1,))
        await callback.message.edit_text(text=f'Ваш регион: {controled_region}\nКоличество курьеров на районе: {couriers_amount}',
                             reply_markup=rm)
    else:
        await callback.message.edit_text(text='Не достаточно прав, обратитесь к администратору')

@admin_profile_router.callback_query(name_callback.filter())
async def name_employee_buttons(callback : types.CallbackQuery, callback_data : name_callback):
    names, other_data = get_employees()
    rm = get_back_to_panel()
    for index, item in enumerate(other_data):
        if item[0] == callback_data.name:
            courier_reg = reg_id_to_str(item[0])
            if item[9] == None:
                await callback.message.edit_text(text=f'ФИО: {item[0]}\nНомер паспорта: {item[1]}\nСерия паспорта: {item[2]}\nТелефон: {item[3]}\nID Telegram: {item[4]}\nОбщее количество заказов: {item[5]}\nЗаказов за день: {item[6]}\nОбщий заработок: {item[7]}\nРегион: {courier_reg}\nРейтинг: Отсутствует', reply_markup=rm)
            else:
                await callback.message.edit_text(text=f'ФИО: {item[0]}\nНомер паспорта: {item[1]}\nСерия паспорта: {item[2]}\nТелефон: {item[3]}\nID Telegram: {item[4]}\nОбщее количество заказов: {item[5]}\nЗаказов за день: {item[6]}\nОбщий заработок: {item[7]}\nРегион: {courier_reg}\nРейтинг: {item[9]}', reply_markup=rm)

