from aiogram import Dispatcher, Bot, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from important_data.config import TOKEN

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)