import sqlite3
import os



def get_employee_attr(telegram_id):
    # Получаем абсолютный путь к базе данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    print(f"Используемый путь к базе данных: {db_path}")  # Для отладки
    conn = sqlite3.connect(db_path)
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


#Обовление кол-ва курьеровна каждом регионе
def set_update_courier_amount():
    # Получаем абсолютный путь к базе данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Получаем все регионы из таблицы Admin и считаем курьеров для каждого региона
    cursor.execute("SELECT id, controled_region FROM Admin")
    admins = cursor.fetchall()

    for admin_id, controled_region in admins:
        #Подсчитываем количество курьеров в таблице Employee, которые работают в этом регионе
        cursor.execute("SELECT COUNT(*) FROM Employee WHERE Region_id = ?", (controled_region,))
        courier_count = cursor.fetchone()[0]
        #Обновляем поле courier_amount для каждого админа
        cursor.execute("UPDATE Admin SET courier_amount = ? WHERE id = ?", (courier_count, admin_id))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

#Проверка на админа
def admin_valid(telegram_id):
    # Получаем абсолютный путь к базе данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, telegram_id FROM Admin")
    admins_ids = cursor.fetchall()
    for id, t_id in admins_ids:
        if int(t_id) == int(telegram_id):
            return True
    return False

def reg_id_to_str(name):
    # Получаем абсолютный путь к базе данных
    set_update_courier_amount()
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT Region_id FROM Employee WHERE Name = ?", (name,))
    region = cursor.fetchone()[0]

    cursor.execute("SELECT Region FROM Regions WHERE № = ?", (region,))
    region = cursor.fetchone()[0]
    return region

def get_admin_panel_data(telegram_id):
    # Получаем абсолютный путь к базе данных
    set_update_courier_amount()
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT controled_region, courier_amount FROM Admin WHERE telegram_id = ?", (telegram_id,))
    region, courier_amount = cursor.fetchone()

    cursor.execute("SELECT Region FROM Regions WHERE № = ?", (region, ))
    region = cursor.fetchone()[0]

    return region, courier_amount

def get_employees():
    # Получаем абсолютный путь к базе данных
    set_update_courier_amount()
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT Name, №Pas, SerPas, Telefon, TgId, ZakazAll, ZakazDay, ZarabotokAll, Region_id, Rating FROM Employee")
    data = cursor.fetchall()
    employee_name_list = []
    employee_other_list = []
    for name in data:
        employee_name_list.append(name[0])
    for item in data:
        employee_other_list.append(item)
    return employee_name_list,  employee_other_list


def create_or_update_data_for_sys(item, column, telegram_id):
    # Получаем абсолютный путь к базе данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/sys.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Проверяем, есть ли запись для текущего пользователя (по telegram_id)
    cursor.execute("SELECT id FROM data WHERE telegram_id = ? ORDER BY id DESC LIMIT 1", (telegram_id,))
    row = cursor.fetchone()

    if row:
        # Если запись найдена, обновляем её
        record_id = row[0]
        cursor.execute(f'UPDATE data SET {column} = ? WHERE id = ?', (item, record_id))
    else:
        # Если записи нет, создаём новую с привязкой к telegram_id
        cursor.execute(f'INSERT INTO data ({column}, telegram_id) VALUES (?, ?)', (item, telegram_id))

    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем соединение