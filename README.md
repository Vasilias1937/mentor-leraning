# СкладПРО - Платформа для аренды складских помещений

Веб-приложение для аренды складских помещений с системой бронирования, управления объявлениями и администрирования.

## 🚀 Возможности

- **Регистрация и аутентификация** пользователей с разными ролями (арендатор, арендодатель, администратор)
- **Создание и управление объявлениями** о складских помещениях
- **Система бронирования** с проверкой доступности дат
- **Дополнительные услуги** для каждого помещения
- **Email-уведомления** о бронированиях
- **Админ-панель** для модерации и управления
- **Адаптивный дизайн** для мобильных устройств

## 🛠 Технологии

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Jinja2, HTML5, CSS3, JavaScript
- **База данных**: MySQL/PostgreSQL
- **Email**: Flask-Mail
- **Docker**: Docker Compose для развертывания

## 📋 Требования

- Python 3.8+
- MySQL 8.0+ или PostgreSQL 12+
- Docker и Docker Compose (опционально)

## 🚀 Быстрый старт

### Вариант 1: С использованием Docker (рекомендуется)

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/warehouse-rental.git
cd warehouse-rental
```

2. **Создайте файл .env:**
```bash
cp .env.example .env
```

3. **Настройте переменные окружения в .env:**
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://user:password@db:3306/real_estate_db
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

4. **Запустите приложение:**
```bash
docker-compose up -d
```

5. **Откройте браузер:**
```
http://localhost:5000
```

### Вариант 2: Локальная установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/warehouse-rental.git
cd warehouse-rental
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте базу данных:**
```bash
# Создайте базу данных MySQL
mysql -u root -p < init.sql
```

5. **Создайте файл .env:**
```bash
cp .env.example .env
```

6. **Настройте переменные окружения в .env:**
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://username:password@localhost/real_estate_db
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

7. **Инициализируйте базу данных:**
```bash
python init_db.py
```

8. **Запустите приложение:**
```bash
python run.py
```

9. **Откройте браузер:**
```
http://localhost:5000
```

## 📊 Структура базы данных

База данных содержит следующие основные таблицы:

- **users** - пользователи системы
- **listings** - объявления о помещениях
- **bookings** - бронирования
- **additional_services** - дополнительные услуги
- **listing_images** - изображения помещений
- **booking_services** - услуги в бронированиях

### Дамп базы данных

Для быстрого восстановления базы данных используйте файл `init.sql`, который содержит:
- Создание всех таблиц
- Настройку индексов и связей
- Тестового администратора (admin@admin.com / admin123)

## 👥 Роли пользователей

### Арендатор (tenant)
- Просмотр каталога помещений
- Создание бронирований
- Управление своими бронированиями

### Арендодатель (landlord)
- Создание и редактирование объявлений
- Управление своими помещениями
- Подтверждение/отклонение бронирований

### Администратор (admin)
- Модерация пользователей и объявлений
- Доступ к админ-панели
- Просмотр статистики

## 📧 Настройка email

Для работы email-уведомлений настройте SMTP в файле `.env`:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 🔧 Конфигурация

Основные настройки находятся в файле `config.py`:

- Размер загружаемых файлов
- Настройки безопасности
- Параметры пагинации
- Настройки почты

## 📁 Структура проекта

```
warehouse-rental/
├── app.py                 # Основное приложение Flask
├── models.py              # Модели SQLAlchemy
├── auth.py                # Аутентификация
├── listings.py            # Управление объявлениями
├── bookings.py            # Система бронирования
├── admin.py               # Админ-панель
├── forms.py               # Формы
├── email_utils.py         # Email-утилиты
├── config.py              # Конфигурация
├── init_db.py             # Инициализация БД
├── init.sql               # Дамп базы данных
├── requirements.txt       # Зависимости Python
├── docker-compose.yml     # Docker Compose
├── Dockerfile             # Docker образ
├── templates/             # HTML шаблоны
├── static/                # Статические файлы
└── logs/                  # Логи приложения
```

## 🧪 Тестирование

Запустите тесты:
```bash
python tests.py
```

## 📝 Логирование

Логи сохраняются в папке `logs/` и содержат информацию о:
- Ошибках приложения
- Действиях пользователей
- Email-уведомлениях

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT.

## 🆘 Поддержка

Если у вас возникли вопросы или проблемы:
1. Проверьте раздел [Issues](https://github.com/your-username/warehouse-rental/issues)
2. Создайте новую issue с описанием проблемы
3. Опишите шаги для воспроизведения ошибки

## 🔐 Безопасность

- Все пароли хешируются с использованием Werkzeug
- Сессии защищены от CSRF атак
- Валидация всех входных данных
- Защита от SQL-инъекций через SQLAlchemy

---

**СкладПРО** - современное решение для аренды складских помещений 🏭 