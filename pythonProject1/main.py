import asyncio

from aiogram import Dispatcher, Bot, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from important_data.config import TOKEN

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)

async def main():
    await dp.start_polling(bot, skip_updates=True)

#bot start
if __name__ == "__main__":
    asyncio.run(main())