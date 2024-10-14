from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline import get_callback_buttons, get_region_buttons, get_profile_button, \
    region_callback
from utils.menu_processing import get_menu_content

courier_profile_router = Router()

@courier_profile_router.message(Command('profile'))
async def profile(message : Message):
    reply_markup, text = get_menu_content(level=0, menu_name="main")
    await message.answer(
        text=text,
        reply_markup=reply_markup
    )

@courier_profile_router.callback_query(region_callback.filter())
async def region_change(callback : types.CallbackQuery, callback_data : region_callback):
    reply_markup, text = get_menu_content(level=callback_data.level, menu_name=callback_data.menu_name)
    await callback.message.edit_text(
        text=text,
        reply_markup=reply_markup
    )
