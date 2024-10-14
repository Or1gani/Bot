from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline import get_callback_buttons, get_region_buttons, get_profile_button, \
    region_callback
from utils.menu_processing import get_menu_content

admin_profile_router = Router()

