import asyncio
from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline import get_callback_buttons
from keyboards.reply import get_buttons
from utils.db_data import (check_id_in_db, count_orders_by_region, regionid_to_regionname,
                           get_random_order, get_order_data, set_cancel_order, set_status)

courier_router = Router()

@courier_router.message(Command('order'))
async def take_order(message : Message):
    #Добавить проверку на то, сколько активных заказов, если активных заказов больше 1, то запретить дальнейшее выполнение
    tg_id = int(message.from_user.id)
    if check_id_in_db(tg_id):
        orders_on_reg = count_orders_by_region(tg_id)
        if orders_on_reg != 0:
            reg_name = regionid_to_regionname(orders_on_reg)
            await message.answer(
                F"Ваш район: {reg_name}\nКоличество заказов на вашем районе: {orders_on_reg}",
                reply_markup=get_callback_buttons(
                    buttons={
                        'Взять заказ' : 'take_order'},
                    sizes=(1,)
                )
            )
        else:
            await message.answer(
                F"Количество заказов на вашем районе: 0"
            )
    else:
        await message.answer("Ваш id телеграм не зарегестрирован в базе данных. Обратитесь к администатору")

# Хранение задач для каждого сообщения
delete_tasks = {}

@courier_router.callback_query(F.data == 'take_order')
async def take_order(callback : CallbackQuery):
    data = get_random_order(callback.from_user.id)
    print(data)
    set_status(data[0], 2)
    text = f"Откуда: {data[1]}\nКуда: {data[2]}\nНомер заказа: {data[0]}"
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
    delay = 10
    delete_task = asyncio.create_task(delete_message_after_delay(callback, msg, delay))
    # Сохраняем задачу, чтобы можно было её отменить
    delete_tasks[msg.message_id] = delete_task



async def delete_message_after_delay(callback: CallbackQuery, msg: Message, delay: int):
    await asyncio.sleep(delay)

    # Проверяем, существует ли сообщение и не была ли задача отменена
    if msg.message_id in delete_tasks:
        try:
            await msg.delete()
            data = get_order_data(callback.from_user.id)
            set_cancel_order(callback.from_user.id)
            await callback.message.answer(
                f"Вы не подтвердили, что находитесь в пути - заказ №{data[0]} отменен."
            )
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")

@courier_router.callback_query(F.data == 'go')
async def go(callback : CallbackQuery):
    # Если пользователь нажал "В путь", отменяем задачу удаления сообщения

    msg_id = callback.message.message_id
    data = get_order_data(callback.from_user.id)
    set_status(data[0], 3)
    text = f"Откуда: {data[1]}\nКуда: {data[2]}\nНомер заказа: {data[0]}"

    if msg_id in delete_tasks:
        delete_tasks[msg_id].cancel()
        del delete_tasks[msg_id]  # Убираем задачу из списка
    await callback.message.edit_text(text=text,
        reply_markup=get_callback_buttons(
            buttons={
              'Подтверить получение заказа':'confirm'
            },
            sizes=(1,)
        )
    )

@courier_router.callback_query(F.data == 'confirm')
async def confirm(callback : CallbackQuery):
    data = get_order_data(callback.from_user.id)
    text = f"Откуда: {data[1]}\nКуда: {data[2]}\nНомер заказа: {data[0]}"
    set_status(data[0],4)
    await callback.message.edit_text(
        text=text,
            reply_markup=get_callback_buttons(buttons={
                'Заказ отдан клиенту' : 'complete'
            },
            sizes=(1,)
        )
    )

@courier_router.callback_query(F.data == 'complete')
async def confirm(callback : CallbackQuery):
    data = get_order_data(callback.from_user.id)
    text = f"Откуда: {data[1]}\nКуда: {data[2]}\nНомер заказа: {data[0]}"
    set_status(data[0], 5)
    await callback.message.edit_text(
        text=text
    )
    await callback.message.answer("Заказ выполнен!", reply_markup=types.ReplyKeyboardRemove())