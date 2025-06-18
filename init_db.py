import mysql.connector
import os

def init_database():
    # Подключаемся к локальному MySQL серверу
    conn = mysql.connector.connect(
        host="db",  # Имя сервиса MySQL в docker-compose.yml
        port=3306,
        user="user",
        password="password",
        database="real_estate_db"
    )
    cursor = conn.cursor()

    try:
        # Читаем SQL скрипт
        with open('init.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # Выполняем SQL скрипт
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        print("База данных успешно инициализирована!")

    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    init_database() 