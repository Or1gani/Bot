import asyncio

from aiogram import Dispatcher, Bot, F, types
from aiogram.types import Message
from important_data.config import TOKEN, conn_params # параметры подключения к бд

from courier_panel.courier import courier_router
from utils.menu_button import Command_manager


bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(courier_router) #Подключение роутера из панели курьера к диспачеру

c_start = types.BotCommand(command='start', description='Запуск бота!')
c_1 = types.BotCommand(command='s1', description='!!!!')
#c_2 = types.BotCommand(command='s2', description='????')



#/start - команда запуска бота
@dp.message(F.text.lower() == "/start")
async def start_command(message : Message):
    await bot.delete_my_commands()
    await Command_manager.take_commands()
    await Command_manager.setup_commands(bot)
    await Command_manager.setup_menu(bot, message)
    await message.answer(F"Привет, {message.from_user.first_name}!")

#основная функция запуска бота
async def main():
    print("ON AIR")
    await dp.start_polling(bot, skip_updates=True)


#bot start
if __name__ == "__main__":
    asyncio.run(main())
