from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline import get_callback_buttons, get_region_buttons, get_profile_button,  \
    region_callback
from utils.menu_processing import get_menu_content
from utils.db_data import set_ticket_data, is_ticket_exsist, get_employee_data



courier_profile_router = Router()

@courier_profile_router.message(Command('profile'))
async def profile(message : Message):
    name, region_name, all_orders, day_orders, cash, rating = get_employee_data(message.from_user.id)
    text = f"{name}\nВаш район: {region_name}\nВыдано заказов всего: {all_orders}\nВыдано заказов за сегодня: {day_orders}\nОбщий заработок: {cash}\n\nРейтинг: {rating}"
    reply_markup, t = get_menu_content(level=0, menu_name="main")
    await message.answer(
        text=text,
        reply_markup=reply_markup
    )

@courier_profile_router.callback_query(region_callback.filter(F.yes == "False"))
async def region_change(callback : types.CallbackQuery, callback_data : region_callback):
    print(callback_data.level, callback_data.menu_name)
    reply_markup, text = get_menu_content(level=callback_data.level, menu_name=callback_data.menu_name)
    await callback.message.edit_text(
        text=text,
        reply_markup=reply_markup
    )


@courier_profile_router.callback_query(region_callback.filter(F.yes == "True"))
async def create_ticket(callback : types.CallbackQuery, callback_data: region_callback):
    if is_ticket_exsist(callback.from_user.id):
        set_ticket_data(callback.from_user.id, callback_data.menu_name)
        await callback.message.edit_text("Запрос отправлен на обработку администратором")
    else:
        await callback.message.edit_text("Ваш тикет уже создан")




