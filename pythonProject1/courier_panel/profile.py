from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from pythonProject1.keyboards.inline import get_callback_buttons, get_region_buttons, get_profile_button
from pythonProject1.utils.menu_processing import get_menu_content

courier_profile_router = Router()

@courier_profile_router.message(Command('profile'))
async def profile(message : Message):
    reply_markup = get_menu_content(level=0)
    await message.answer(
        F"Имя Фамилия\nВаш район: (название)\nВыдано заказов всего: (число)\nВыдано заказов за сегодня: (число)\nОбщий заработок: (число заказов * коэффициент)\n\nРейтинг: (0-5*)",
        reply_markup=reply_markup
    )

@courier_profile_router.callback_query(F.data == 'change_region')
async def change_region(callback : CallbackQuery):
    await callback.message.edit_text(
        F"В настоящее время доступны следующие районы:",
        reply_markup=get_region_buttons(
            level=0
        )
    )