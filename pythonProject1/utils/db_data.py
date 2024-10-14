import sqlite3

def get_employee_attr(telegram_id):
    conn = sqlite3.connect('../DataBase/Kura.db')
    cursor = conn.cursor()
    # Выполняем запрос к таблице
    cursor.execute(f'SELECT Name, Telefon, ZakazAll, ZakazDay FROM Employee WHERE № = {telegram_id}')

    # Извлекаем результат
    result = cursor.fetchone()
    print(result)
    if result:
        name, number, all_orders, daily_orders = result
    else:
        name = ""
        number = ""
        all_orders = 0
        daily_orders = 0

    # Закрываем соединение
    conn.close()
    return name, number, all_orders, daily_orders
get_employee_attr()