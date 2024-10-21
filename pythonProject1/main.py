import asyncio

from aiogram import Dispatcher, Bot, F, types
from aiogram.types import Message
from important_data.config import TOKEN, API_ID, API_HASH# параметры подключения к бд

from courier_panel.courier import courier_router
from courier_panel.profile import courier_profile_router
from admin_panel.admin import admin_router
from admin_panel.profile import admin_profile_router

from utils.menu_button import Command_manager, CourierCommandManager, AdminCommandManager
from utils.db_data import admin_valid

from pyrogram import Client

app = Client("my_bot", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH)

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_routers(courier_router, courier_profile_router, admin_router, admin_profile_router) #Подключение роутера из панелей к диспачеру
ccm = CourierCommandManager() #Экзепляр меню для курьера
acm = AdminCommandManager() #Экзепляр меню для админа

'''
async def get_user_id(username: str) -> int:
    if username.startswith('@'):
        try:
            user = await app.get_users(username)
            return user.id
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return None
    else:
        print("Юзернейм должен начинаться с '@'.")
        return None

@dp.message()
async def start_command(message: Message):
    user_id = await get_user_id(message.text)
    if user_id is not None:
        await message.answer(f"ID пользователя: {user_id}")
    else:
        await message.answer("Не удалось получить ID пользователя.")
'''

#/start - команда запуска бота
@dp.message(F.text.lower() == "/start")
async def start_command(message : Message):
    t_id = message.from_user.id
    if admin_valid(t_id):
        await bot.delete_my_commands()
        await acm.setup_commands(bot=bot)
        await acm.setup_menu(bot=bot, message=message)
        await message.answer(F"Привет, {message.from_user.first_name}! Вы Администратор")
    else:
        await bot.delete_my_commands()
        await ccm.setup_commands(bot=bot)
        await ccm.setup_menu(bot=bot, message=message)
        await message.answer(F"Привет, {message.from_user.first_name}! Вы Курьер")

#основная функция запуска бота
async def main():
    print("ON AIR")
    await app.start()  # Запускаем клиент
    await dp.start_polling(bot, skip_updates=True)


#bot start
if __name__ == "__main__":
    asyncio.run(main())
