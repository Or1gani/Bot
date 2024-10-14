import psycopg2
from important_data.config import conn_params

try:
    print("Попытка подключения...")
    # Подключаемся к базе данных
    conn = psycopg2.connect(**conn_params)
    print("Подключение успешно!")

    # Создаем курсор
    cursor = conn.cursor()
    print("Курсор создан, выполняем запрос...")

    # Выполняем запрос для подсчета строк

    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM materface")
        print("Запрос выполнен, получаем данные...")
        # Получаем результат запроса
        row_count = cursor.fetchone()
        print(f"Количество строк: {row_count[0]}")

    # Закрываем соединение
    cursor.close()
    print("Курсор закрыт.")
    conn.close()
    print("Соединение закрыто.")

except Exception as e:
    print(f"Ошибка подключения: {e}")