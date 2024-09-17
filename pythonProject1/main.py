import asyncio

from aiogram import Dispatcher, Bot, F, types
from aiogram.types import Message
from important_data.config import TOKEN, conn_params # параметры подключения к бд

from courier_panel.courier import courier_router


bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(courier_router) #Подключение роутера из панели курьера к диспачеру

#/start - команда запуска бота
@dp.message(F.text.lower() == "/start")
async def start_command(message : Message):
    await message.answer(F"Привет, {message.from_user.first_name}!")

#основная функция запуска бота
async def main():
    await dp.start_polling(bot, skip_updates=True)

#bot start
if __name__ == "__main__":
    asyncio.run(main())