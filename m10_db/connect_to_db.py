import sqlite3

# Подключаемся к базе данных
DB_PATH = "/Users/veranikalis/Geekbrains/ПРОГРАММИСТ/PYTHON/Flask/m10_db/sample02.db"

def connect_to_db():
    # Устанавливаем соединение с базой
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Выполняем запрос
    cursor.execute("SELECT * FROM clients")
    result = cursor.fetchall()

    # Выводим результат
    for row in result:
        print(row)

    # Закрываем соединение
    conn.close()

if __name__ == "__main__":
    connect_to_db()