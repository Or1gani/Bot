from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.db_data import reset_daily_orders  # Подставьте вашу функцию для работы с БД

def schedule_daily_reset():
    scheduler = AsyncIOScheduler()
    #scheduler.add_job(reset_daily_orders, 'interval', minutes=1) #Рабочее, каждую минуту очищает заказы за день
    scheduler.add_job(reset_daily_orders, 'cron', hour=0, minute=0)
    scheduler.start()