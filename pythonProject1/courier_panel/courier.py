from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from pythonProject1.keyboards.inline import get_callback_buttons

courier_router = Router()

@courier_router.message(Command('order'))
async def take_order(message : Message):
    await message.answer(
        F"Ваш район: Хорошевский р-н\nКоличество заказов: 10",
        reply_markup=get_callback_buttons(
            buttons={
                'Взять заказ' : 'take_order'},
            sizes=(1,)
        )
    )

@courier_router.callback_query(F.data == 'take_order')
async def take_order(callback : CallbackQuery):
    await callback.message.edit_text(
        "Откуда: (название ресторана), (адрес)\nКуда: (адрес клиента)\n(Комментарий клиента)\nНомер заказа(служебная инфа)",
        reply_markup=get_callback_buttons(
            buttons={
                'В путь' : 'go'},
            sizes=(1,)
        )
    )

@courier_router.callback_query(F.data == 'go')
async def go(callback : CallbackQuery):
    await callback.message.edit_text(
        "Откуда: (название ресторана), (адрес)\nКуда: (адрес клиента)\n(Комментарий клиента)\nномер заказа(служебная инфа)",
        reply_markup=get_callback_buttons(
            buttons={
              'Подтверить получение заказа':'confirm'
            },
            sizes=(1,)
        )
    )

@courier_router.callback_query(F.data == 'confirm')
async def confirm(callback : CallbackQuery):
    await callback.message.edit_text(
        "Откуда: (название ресторана), (адрес)\nКуда: (адрес клиента)\n(Комментарий клиента)\nномер заказа(служебная инфа)",
            reply_markup=get_callback_buttons({
                'Заказ отдан клиенту' : 'complete' #####
            },
            sizes=(1,)
        )
    )