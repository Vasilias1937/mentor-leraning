#!/usr/bin/env python3
"""
Скрипт для автоматической настройки проекта СкладПРО
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - выполнено успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ошибка: {e.stderr}")
        return False

def create_env_file():
    """Создает файл .env из примера"""
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            shutil.copy('env.example', '.env')
            print("✅ Файл .env создан из env.example")
            print("⚠️  Не забудьте настроить переменные окружения в файле .env")
        else:
            print("❌ Файл env.example не найден")
            return False
    else:
        print("ℹ️  Файл .env уже существует")
    return True

def create_upload_dirs():
    """Создает необходимые директории для загрузки файлов"""
    upload_dirs = [
        'static/uploads',
        'static/uploads/covers',
        'logs'
    ]
    
    for dir_path in upload_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Создана директория: {dir_path}")

def check_python_version():
    """Проверяет версию Python"""
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        return False
    print(f"✅ Версия Python: {sys.version}")
    return True

def install_dependencies():
    """Устанавливает зависимости Python"""
    if not run_command("pip install -r requirements.txt", "Установка зависимостей Python"):
        return False
    return True

def setup_database():
    """Настраивает базу данных"""
    print("📊 Настройка базы данных...")
    print("ℹ️  Убедитесь, что MySQL/PostgreSQL запущен и доступен")
    print("ℹ️  Создайте базу данных и пользователя согласно init.sql")
    
    # Проверяем наличие init_db.py
    if os.path.exists('init_db.py'):
        print("ℹ️  Для инициализации базы данных выполните: python init_db.py")
    else:
        print("ℹ️  Для создания таблиц выполните: mysql -u root -p < init.sql")

def main():
    """Основная функция настройки"""
    print("🚀 Настройка проекта СкладПРО")
    print("=" * 50)
    
    # Проверяем версию Python
    if not check_python_version():
        sys.exit(1)
    
    # Создаем файл .env
    if not create_env_file():
        sys.exit(1)
    
    # Создаем директории
    create_upload_dirs()
    
    # Устанавливаем зависимости
    if not install_dependencies():
        print("❌ Ошибка при установке зависимостей")
        sys.exit(1)
    
    # Настраиваем базу данных
    setup_database()
    
    print("\n" + "=" * 50)
    print("✅ Настройка завершена!")
    print("\n📋 Следующие шаги:")
    print("1. Настройте переменные окружения в файле .env")
    print("2. Создайте базу данных и выполните init.sql")
    print("3. Запустите приложение: python run.py")
    print("\n🌐 Приложение будет доступно по адресу: http://localhost:5000")
    print("👤 Тестовый администратор: admin@admin.com / admin123")

if __name__ == "__main__":
    main() 