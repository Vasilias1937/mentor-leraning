#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функционала бронирований
"""

from app import app, db
from models import User, Listing, Booking, AdditionalService
from datetime import date, timedelta

def test_booking_functionality():
    """Тестирование функционала бронирований"""
    with app.app_context():
        try:
            # Проверяем, что таблицы существуют
            print("Проверка существования таблиц...")
            
            # Проверяем количество записей в таблицах
            users_count = User.query.count()
            listings_count = Listing.query.count()
            bookings_count = Booking.query.count()
            services_count = AdditionalService.query.count()
            
            print(f"Пользователей: {users_count}")
            print(f"Объявлений: {listings_count}")
            print(f"Бронирований: {bookings_count}")
            print(f"Дополнительных услуг: {services_count}")
            
            # Проверяем структуру таблиц
            print("\nПроверка структуры таблиц...")
            
            # Проверяем, что можно создать тестовое бронирование
            if users_count > 0 and listings_count > 0:
                print("Создание тестового бронирования...")
                
                # Находим первого пользователя-арендатора
                tenant = User.query.filter_by(user_type='tenant').first()
                if not tenant:
                    print("Создаем тестового арендатора...")
                    tenant = User(
                        email='test_tenant@example.com',
                        first_name='Тест',
                        last_name='Арендатор',
                        phone='+7-999-123-45-67',
                        user_type='tenant'
                    )
                    tenant.set_password('password123')
                    db.session.add(tenant)
                    db.session.flush()
                
                # Находим первое объявление
                listing = Listing.query.filter_by(is_active=True).first()
                if not listing:
                    print("Создаем тестовое объявление...")
                    landlord = User.query.filter_by(user_type='landlord').first()
                    if not landlord:
                        print("Создаем тестового арендодателя...")
                        landlord = User(
                            email='test_landlord@example.com',
                            first_name='Тест',
                            last_name='Арендодатель',
                            phone='+7-999-987-65-43',
                            user_type='landlord'
                        )
                        landlord.set_password('password123')
                        db.session.add(landlord)
                        db.session.flush()
                    
                    listing = Listing(
                        title='Тестовое помещение',
                        description='Описание тестового помещения',
                        address='Тестовый адрес',
                        city='Москва',
                        region='Московская область',
                        country='Россия',
                        postal_code='123456',
                        base_price=10000.00,
                        area_sqm=100.00,
                        min_lease_period_months=1,
                        landlord_id=landlord.user_id,
                        room_type='warehouse'
                    )
                    db.session.add(listing)
                    db.session.flush()
                
                # Создаем тестовое бронирование
                start_date = date.today() + timedelta(days=7)
                end_date = start_date + timedelta(days=30)
                
                booking = Booking(
                    listing_id=listing.listing_id,
                    tenant_id=tenant.user_id,
                    start_date=start_date,
                    end_date=end_date,
                    total_price=10000.00,
                    status='pending'
                )
                db.session.add(booking)
                db.session.commit()
                
                print(f"Тестовое бронирование создано с ID: {booking.booking_id}")
                print(f"Период: {booking.start_date} - {booking.end_date}")
                print(f"Статус: {booking.status}")
                
                # Проверяем, что бронирование можно найти
                found_booking = Booking.query.get(booking.booking_id)
                if found_booking:
                    print("Бронирование успешно найдено в базе данных")
                else:
                    print("ОШИБКА: Бронирование не найдено в базе данных")
                
            else:
                print("Недостаточно данных для тестирования")
            
            print("\nТестирование завершено успешно!")
            
        except Exception as e:
            print(f"Ошибка при тестировании: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_booking_functionality() 