#!/usr/bin/env python3
"""
Скрипт для тестирования подключения к базе данных
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def test_connection():
    """Тестирует подключение к базе данных"""
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Переменная DATABASE_URL не найдена в .env файле")
        return False
    
    print(f"🔗 Подключение к базе данных: {database_url.split('@')[1] if '@' in database_url else database_url}")
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Подключение к базе данных успешно!")
            return True
    except SQLAlchemyError as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def test_tables():
    """Проверяет наличие основных таблиц"""
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Переменная DATABASE_URL не найдена в .env файле")
        return False
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Проверяем наличие основных таблиц
            tables = ['users', 'listings', 'bookings', 'additional_services', 'listing_images', 'booking_services']
            
            for table in tables:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"✅ Таблица {table}: {count} записей")
                except SQLAlchemyError as e:
                    print(f"❌ Таблица {table} не найдена или недоступна: {e}")
                    return False
            
            return True
    except Exception as e:
        print(f"❌ Ошибка при проверке таблиц: {e}")
        return False

def test_admin_user():
    """Проверяет наличие администратора в системе"""
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Переменная DATABASE_URL не найдена в .env файле")
        return False
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users WHERE user_type = 'admin'"))
            admin_count = result.scalar()
            
            if admin_count > 0:
                print(f"✅ Найдено администраторов: {admin_count}")
                
                # Получаем информацию об администраторах
                result = conn.execute(text("SELECT email, first_name, last_name FROM users WHERE user_type = 'admin'"))
                admins = result.fetchall()
                
                for admin in admins:
                    print(f"   👤 {admin[0]} ({admin[1]} {admin[2]})")
                
                return True
            else:
                print("⚠️  Администраторы не найдены")
                return False
    except Exception as e:
        print(f"❌ Ошибка при проверке администраторов: {e}")
        return False

def test_sample_data():
    """Проверяет наличие тестовых данных"""
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Переменная DATABASE_URL не найдена в .env файле")
        return False
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Проверяем количество записей в основных таблицах
            tables_data = [
                ('users', 'пользователей'),
                ('listings', 'объявлений'),
                ('bookings', 'бронирований'),
                ('additional_services', 'дополнительных услуг')
            ]
            
            print("\n📊 Статистика базы данных:")
            for table, description in tables_data:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"   📋 {description.capitalize()}: {count}")
                except SQLAlchemyError:
                    print(f"   ❌ Ошибка при подсчете {description}")
            
            return True
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование базы данных СкладПРО")
    print("=" * 50)
    
    # Тест подключения
    if not test_connection():
        print("\n❌ Тестирование прервано из-за ошибки подключения")
        sys.exit(1)
    
    # Тест таблиц
    if not test_tables():
        print("\n❌ Тестирование прервано из-за ошибки таблиц")
        sys.exit(1)
    
    # Тест администратора
    test_admin_user()
    
    # Тест данных
    test_sample_data()
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено успешно!")
    print("\n💡 Если все тесты прошли успешно, база данных готова к работе")
    print("🌐 Запустите приложение: python run.py")

if __name__ == "__main__":
    main() 