from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_buttons(
        *,
        buttons: list[str],
        sizes: tuple[int] = (2,)):

    keyboard = ReplyKeyboardBuilder()

    for text in buttons:
        keyboard.add(KeyboardButton(text=text))
    return keyboard.adjust(*sizes).as_markup()
