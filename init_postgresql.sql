-- Инициализация базы данных для PostgreSQL на Render
-- СкладПРО - Платформа для аренды складских помещений

-- Создание таблицы пользователей
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    user_type VARCHAR(20) CHECK (user_type IN ('tenant', 'landlord', 'admin')) NOT NULL,
    company_name VARCHAR(100),
    tax_id VARCHAR(50),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы профилей пользователей
CREATE TABLE user_profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    user_url VARCHAR(255),
    description TEXT,
    rating DECIMAL(3,2)
);

-- Создание таблицы объявлений
CREATE TABLE listings (
    listing_id SERIAL PRIMARY KEY,
    landlord_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    address TEXT NOT NULL,
    city VARCHAR(100),
    region VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    base_price DECIMAL(10,2) NOT NULL,
    area_sqm DECIMAL(10,2) NOT NULL,
    min_lease_period_months INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    room_type VARCHAR(20) CHECK (room_type IN ('freezer', 'warehouse', 'production')) NOT NULL DEFAULT 'warehouse'
);

-- Создание таблицы дополнительных услуг
CREATE TABLE additional_services (
    service_id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES listings(listing_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL
);

-- Создание таблицы изображений помещений
CREATE TABLE listing_images (
    image_id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES listings(listing_id) ON DELETE CASCADE,
    image_url VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    sort_order INTEGER DEFAULT 0
);

-- Создание таблицы бронирований
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES listings(listing_id) ON DELETE CASCADE,
    tenant_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed')) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы услуг в бронированиях
CREATE TABLE booking_services (
    booking_service_id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    service_id INTEGER NOT NULL REFERENCES additional_services(service_id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1,
    total_price DECIMAL(10,2) NOT NULL
);

-- Создание индексов для улучшения производительности
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_user_type ON users(user_type);
CREATE INDEX idx_listings_landlord_id ON listings(landlord_id);
CREATE INDEX idx_listings_is_active ON listings(is_active);
CREATE INDEX idx_listings_room_type ON listings(room_type);
CREATE INDEX idx_listings_city ON listings(city);
CREATE INDEX idx_bookings_listing_id ON bookings(listing_id);
CREATE INDEX idx_bookings_tenant_id ON bookings(tenant_id);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_dates ON bookings(start_date, end_date);
CREATE INDEX idx_listing_images_listing_id ON listing_images(listing_id);
CREATE INDEX idx_additional_services_listing_id ON additional_services(listing_id);

-- Создание триггера для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Применение триггера к таблицам
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_listings_updated_at BEFORE UPDATE ON listings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bookings_updated_at BEFORE UPDATE ON bookings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Добавление тестового администратора
-- Пароль: admin123 (хеш scrypt)
INSERT INTO users (email, password_hash, first_name, last_name, user_type, is_verified)
VALUES (
    'admin@admin.com',
    'scrypt:32768:8:1$VXfFaJtrp7z7D9BI$953f02842661dec561df646e88939efa77c9af1ba17bda2eb1a65d1d766e616a8c2ad44406c98fcddd73e38f4cfaa31dab68a6171ba36ca267efc3e1b78f0620',
    'Admin',
    'Admin',
    'admin',
    TRUE
);

-- Добавление тестовых данных
-- Тестовый арендодатель
INSERT INTO users (email, password_hash, first_name, last_name, user_type, is_verified, company_name)
VALUES (
    'landlord@test.com',
    'scrypt:32768:8:1$VXfFaJtrp7z7D9BI$953f02842661dec561df646e88939efa77c9af1ba17bda2eb1a65d1d766e616a8c2ad44406c98fcddd73e38f4cfaa31dab68a6171ba36ca267efc3e1b78f0620',
    'Иван',
    'Петров',
    'landlord',
    TRUE,
    'ООО "СкладСервис"'
);

-- Тестовый арендатор
INSERT INTO users (email, password_hash, first_name, last_name, user_type, is_verified, company_name)
VALUES (
    'tenant@test.com',
    'scrypt:32768:8:1$VXfFaJtrp7z7D9BI$953f02842661dec561df646e88939efa77c9af1ba17bda2eb1a65d1d766e616a8c2ad44406c98fcddd73e38f4cfaa31dab68a6171ba36ca267efc3e1b78f0620',
    'Анна',
    'Сидорова',
    'tenant',
    TRUE,
    'ИП "ЛогистикаПлюс"'
);

-- Тестовые объявления
INSERT INTO listings (landlord_id, title, description, address, city, region, country, postal_code, base_price, area_sqm, min_lease_period_months, room_type)
VALUES 
(2, 'Склад в центре города', 'Современный склад с отличной транспортной доступностью', 'ул. Ленина, 15', 'Москва', 'Московская область', 'Россия', '123456', 50000.00, 200.00, 6, 'warehouse'),
(2, 'Холодильный склад', 'Специализированный холодильный склад для продуктов питания', 'ул. Промышленная, 45', 'Санкт-Петербург', 'Ленинградская область', 'Россия', '654321', 75000.00, 150.00, 12, 'freezer'),
(2, 'Производственное помещение', 'Помещение для производственных нужд с высокими потолками', 'ул. Заводская, 78', 'Екатеринбург', 'Свердловская область', 'Россия', '543210', 60000.00, 300.00, 3, 'production');

-- Тестовые дополнительные услуги
INSERT INTO additional_services (listing_id, name, description, price)
VALUES 
(1, 'Погрузочно-разгрузочные работы', 'Услуги грузчиков и спецтехники', 5000.00),
(1, 'Охрана', 'Круглосуточная охрана территории', 15000.00),
(2, 'Температурный мониторинг', 'Система контроля температуры', 8000.00),
(3, 'Электроэнергия', 'Дополнительное энергопотребление', 10000.00); 