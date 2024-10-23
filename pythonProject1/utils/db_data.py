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

def regionid_to_regionname(region_id):
    # Получаем абсолютный путь к базе данных
    set_update_courier_amount()
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT Region FROM Regions WHERE № = ?", (region_id,))

    region = cursor.fetchone()[0]
    return region

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

def get_tg_name(admin_id):
    # Получаем абсолютный путь к базе данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/sys.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nick FROM data WHERE telegram_id = ?", (admin_id,))
    nick = cursor.fetchone()
    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем соединение
    return nick[0]


def transfer_data():
    # Подключаемся к исходной и целевой базам данных
    target_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    source_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/sys.db'))
    source_conn = sqlite3.connect(source_db_path)
    target_conn = sqlite3.connect(target_db_path)

    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()

    # Извлекаем данные из таблицы "data"
    source_cursor.execute("SELECT * FROM data")
    rows = source_cursor.fetchall()

    for row in rows:
        # Объединяем name1, name2 и name3 в одно значение для "Name"
        name = f"{row[3]} {row[4]} {row[5]}".strip()  # row[3], row[4], row[5] - соответствуют name1, name2, name3

        # Разбиваем pass на два числа для "№Pas" и "SerPas"
        if row[6]:  # row[6] - pass
            pas_parts = row[6].split()  # разделяем по пробелу
            pas_number = int(pas_parts[0]) if len(pas_parts) > 0 else 0
            ser_number = int(pas_parts[1]) if len(pas_parts) > 1 else 0
        else:
            pas_number = 0
            ser_number = 0

        # Получаем telegram_id
        telegram_id = row[9]  # row[7] - telegram_id
        region = row[8]

        # Вставляем данные в таблицу "Employee"
        target_cursor.execute("""
            INSERT INTO Employee (Name, №Pas, SerPas, TgId, Region_id) 
            VALUES (?, ?, ?, ?, ?)""",
                              (name, pas_number, ser_number, telegram_id, region)
                              )

    # Сохраняем изменения и закрываем соединения
    target_conn.commit()
    source_conn.close()
    target_conn.close()
    print("Данные успешно перенесены!")


def get_region_list():
    # Получаем абсолютный путь к базе данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Region FROM Regions")
    list = cursor.fetchall()
    reg_list = {}
    for id, reg in enumerate(list):
        reg_list[id+1] = reg[0]
    return reg_list


def get_employee_data(tg_id):
    # Получаем абсолютный путь к базе данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Region_id FROM Employee WHERE TgId = ?", (tg_id,))
    region_id = cursor.fetchone()[0]
    cursor.execute("SELECT Region FROM Regions WHERE № = ?", (region_id,))
    region = cursor.fetchone()[0]
    cursor.execute("SELECT Name, ZakazAll, ZakazDay, ZarabotokAll, Rating FROM Employee WHERE TgId = ?", (tg_id,))
    data = cursor.fetchone()
    name, all_orders, day_orders, cash, rating = data[0], data[1], data[2], data[3], data[4]
    return name, region, all_orders, day_orders, cash, rating

def is_ticket_exsist(tg_id):
    # Подключаемся к исходной и целевой базам данных
    sys_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/sys.db'))
    sys_conn = sqlite3.connect(sys_db_path)
    sys_cursor = sys_conn.cursor()
    sys_cursor.execute("SELECT tg_id_employee FROM ticket_region WHERE tg_id_employee = ?", (tg_id,))
    id = sys_cursor.fetchone()
    if id is not None:
        print(id[0])
        return False
    else:
        print(id)
        return True


def set_ticket_data(tg_id, target_region):
    # Подключаемся к исходной и целевой базам данных
    sys_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/sys.db'))
    Kura_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    sys_conn = sqlite3.connect(sys_db_path)
    Kura_conn = sqlite3.connect(Kura_db_path)

    sys_cursor = sys_conn.cursor()
    kura_cursor = Kura_conn.cursor()

    kura_cursor.execute("SELECT Region_id FROM Employee WHERE TgId = ?", (tg_id,))
    current_region = kura_cursor.fetchone()[0]
    sys_cursor.execute('INSERT INTO ticket_region ("tg_id_employee", "from", "to") VALUES (?, ?, ?)', (tg_id, current_region, target_region))

    sys_conn.commit()
    sys_conn.close()
    kura_cursor.close()


def get_tickets():
    # Подключаемся к исходной и целевой базам данных
    sys_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/sys.db'))
    sys_conn = sqlite3.connect(sys_db_path)
    sys_cursor = sys_conn.cursor()
    sys_cursor.execute('SELECT "tg_id_employee", "from", "to" FROM ticket_region')
    tickets = sys_cursor.fetchall()
    print(tickets)
    return tickets

def get_name_by_tg_id(tg_id):
    # Получаем абсолютный путь к базе данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM Employee WHERE TgId = ?", (tg_id,))
    name = cursor.fetchone()
    if name is not None:
        return name[0]
    else:
        print("Ошибка! get_name_by_tg_id - Name = none")


def update_region(tg_id, new_region_id):
    # Получаем абсолютный путь к базе данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/Kura.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE Employee SET Region_id = ? WHERE TgId = ?", (new_region_id, tg_id))
    conn.commit()
    conn.close()

def remove_ticket(tg_id):
    # Получаем абсолютный путь к базе данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase/sys.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ticket_region WHERE tg_id_employee = ?", (tg_id,))
    conn.commit()
    conn.close()