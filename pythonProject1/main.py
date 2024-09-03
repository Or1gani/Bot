import asyncio

from aiogram import Dispatcher, Bot, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from important_data.config import TOKEN

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

@dp.message(F.text.lower() == "/start")
async def start_command(message : Message):
    await message.answer(F"Привет, {message.from_user.first_name}!")

async def main():
    await dp.start_polling(bot, skip_updates=True)

#bot start
if __name__ == "__main__":
    asyncio.run(main())