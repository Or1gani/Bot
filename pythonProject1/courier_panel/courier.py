import asyncio
from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline import get_callback_buttons
from keyboards.reply import get_buttons

courier_router = Router()

@courier_router.message(Command('order'))
async def take_order(message : Message):
    #Добавить проверку на то, сколько активных заказов, если активных заказов больше 1, то запретить дальнейшее выполнение
    await message.answer(
        F"Ваш район: Хорошевский р-н\nКоличество заказов: 10",
        reply_markup=get_callback_buttons(
            buttons={
                'Взять заказ' : 'take_order'},
            sizes=(1,)
        )
    )

# Хранение задач для каждого сообщения
delete_tasks = {}

@courier_router.callback_query(F.data == 'take_order')
async def take_order(callback : CallbackQuery):
    text = "Откуда: (название ресторана), (адрес)\nКуда: (адрес клиента)\n(Комментарий клиента)\nНомер заказа(служебная инфа)"
    msg = await callback.message.edit_text(
        text=text,
        reply_markup=get_callback_buttons(
            buttons={
                'В путь' : 'go'},
            sizes=(1,)
        )
    )
    await callback.answer(
        "Вы взяли заказ!\nВремя на подтверждение получения заказа курьером: 25 минут, иначе заказ отменится.\nДоступен чат с клиентом.",
        reply_markup=get_buttons(
            buttons=["Чат с клиентом","Состав заказа","Профиль"],
            sizes=(2,)
        ),
        show_alert=True
    )
    # Создаем задачу для удаления сообщения через "delay" сек
    delay = 6
    delete_task = asyncio.create_task(delete_message_after_delay(callback, msg, delay))
    # Сохраняем задачу, чтобы можно было её отменить
    delete_tasks[msg.message_id] = delete_task



async def delete_message_after_delay(callback: CallbackQuery, msg: Message, delay: int):
    await asyncio.sleep(delay)

    # Проверяем, существует ли сообщение и не была ли задача отменена
    if msg.message_id in delete_tasks:
        try:
            await msg.delete()
            await callback.message.answer(
                "Вы не подтвердили, что находитесь в пути - заказ (номер заказа) отменен."
            )
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")

@courier_router.callback_query(F.data == 'go')
async def go(callback : CallbackQuery):
    # Если пользователь нажал "В путь", отменяем задачу удаления сообщения
    msg_id = callback.message.message_id

    if msg_id in delete_tasks:
        delete_tasks[msg_id].cancel()
        del delete_tasks[msg_id]  # Убираем задачу из списка
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
            reply_markup=get_callback_buttons(buttons={
                'Заказ отдан клиенту' : 'complete'
            },
            sizes=(1,)
        )
    )

@courier_router.callback_query(F.data == 'complete')
async def confirm(callback : CallbackQuery):
    await callback.message.edit_text(
        "Откуда: (название ресторана), (адрес)\nКуда: (адрес клиента)\n(Комментарий клиента)\nномер заказа(служебная инфа)",
            reply_markup=get_callback_buttons(buttons={
                'Заказ отдан клиенту' : 'end'
            },
            sizes=(1,)
        )
    )
    await callback.message.answer("Заказ выполнен!", reply_markup=types.ReplyKeyboardRemove())