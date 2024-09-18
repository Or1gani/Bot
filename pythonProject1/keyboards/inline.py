from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.filters.callback_data import CallbackData

class region_callback(CallbackData, prefix="region"):
    level: int
    region_name: str | None = None

regions = ['Район 1','Район 2','Район 3','Район 4','Район 5','Район 6','Район 7']

def get_callback_buttons(
        *,
        buttons: dict[str, str],
        sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()

def get_profile_button(*, level: int, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text='Профиль',
         callback_data=region_callback(level=level+1).pack()
    ))
    return keyboard.adjust(*sizes).as_markup()

def get_region_buttons(*, level: int, region_name: str, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text='Назад',
         callback_data=region_callback(level=level-1)
    ))
    for region in regions:
        keyboard.add(InlineKeyboardButton(
            text=region,
            callback_data=region_callback(level=level, region_name=region).pack()
        ))
    return keyboard.adjust(*sizes).as_markup()