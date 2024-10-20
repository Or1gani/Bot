import asyncio

from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline import get_callback_buttons
from keyboards.reply import get_buttons


admin_router = Router()

@admin_router.callback_query(F.data == 'add_employee')
async def set_role(callback: CallbackQuery):
    await callback.message.answer("hi")
