import aiogram
import asyncio
from aiogram import types

class Command_manager:
    def __init__(self):
        self.commands = []
    async def setup_commands(self, bot : aiogram.Bot):
        await bot.set_my_commands(self.commands)
    async def setup_menu(self, bot : aiogram.Bot, message : types.Message):
        await bot.set_chat_menu_button(chat_id=message.chat.id, menu_button=types.MenuButtonCommands(type='commands'))

class CourierCommandManager(Command_manager):
    def __init__(self):
        super().__init__()
        # Добавляем команды для курьеров
        self.commands = [
            types.BotCommand(command='start', description='Запуск бота'),
            types.BotCommand(command='order', description='Просмотр заказов'),
            types.BotCommand(command='profile', description='Ваш профиль')
        ]

class AdminCommandManager(Command_manager):
    def __init__(self):
        super().__init__()
        # Добавляем команды для администраторов
        self.commands = [
            types.BotCommand(command='start', description='Запуск бота'),
            types.BotCommand(command='admin_panel', description='Панель администратора'),
        ]

