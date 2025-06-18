import unittest
from app import app, db
from models import User, Listing, Booking
from werkzeug.security import generate_password_hash

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Создание тестового пользователя
        user = User(
            email='test@example.com',
            password_hash=generate_password_hash('test123'),
            first_name='Test',
            last_name='User',
            phone='+7 (999) 999-99-99',
            user_type='tenant',
            is_verified=True
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.post('/login', data={
            'email': 'test@example.com',
            'password': 'test123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.app.post('/register', data={
            'email': 'new@example.com',
            'password': 'new123',
            'password2': 'new123',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '+7 (999) 888-88-88',
            'user_type': 'tenant'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        user = User.query.filter_by(email='new@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, 'New')

    def test_create_listing(self):
        # Создание арендодателя
        landlord = User(
            email='landlord@example.com',
            password_hash=generate_password_hash('landlord123'),
            first_name='Landlord',
            last_name='User',
            phone='+7 (999) 777-77-77',
            user_type='landlord',
            is_verified=True
        )
        db.session.add(landlord)
        db.session.commit()

        # Вход как арендодатель
        self.app.post('/login', data={
            'email': 'landlord@example.com',
            'password': 'landlord123'
        })

        # Создание объявления
        response = self.app.post('/listings/create', data={
            'title': 'Test Listing',
            'description': 'Test Description',
            'address': 'Test Address',
            'city': 'Test City',
            'region': 'Test Region',
            'country': 'Test Country',
            'postal_code': '123456',
            'base_price': 1000.00,
            'area_sqm': 500.00,
            'min_lease_period_months': 3
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        listing = Listing.query.filter_by(title='Test Listing').first()
        self.assertIsNotNone(listing)
        self.assertEqual(listing.description, 'Test Description')

    def test_booking(self):
        # Создание объявления
        listing = Listing(
            landlord_id=1,
            title='Test Listing',
            description='Test Description',
            address='Test Address',
            city='Test City',
            region='Test Region',
            country='Test Country',
            postal_code='123456',
            base_price=1000.00,
            area_sqm=500.00,
            min_lease_period_months=3,
            is_active=True
        )
        db.session.add(listing)
        db.session.commit()

        # Вход как арендатор
        self.app.post('/login', data={
            'email': 'test@example.com',
            'password': 'test123'
        })

        # Создание бронирования
        response = self.app.post(f'/listings/{listing.listing_id}/book', data={
            'start_date': '2024-01-01',
            'end_date': '2024-02-01'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        booking = Booking.query.filter_by(listing_id=listing.listing_id).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.status, 'pending')

if __name__ == '__main__':
    unittest.main() 