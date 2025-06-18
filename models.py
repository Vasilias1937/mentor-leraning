from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    user_type = db.Column(db.Enum('tenant', 'landlord', 'admin'), nullable=False)
    company_name = db.Column(db.String(100))
    tax_id = db.Column(db.String(50))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    rating = db.Column(db.Numeric(3, 2))

class Listing(db.Model):
    __tablename__ = 'listings'
    
    listing_id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100))
    region = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    area_sqm = db.Column(db.Numeric(10, 2), nullable=False)
    min_lease_period_months = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    room_type = db.Column(db.Enum('freezer', 'warehouse', 'production'), nullable=False)

    images = db.relationship('ListingImage', backref='listing', lazy=True, cascade='all, delete-orphan')
    landlord = db.relationship('User', backref='listings', lazy=True)
    additional_services = db.relationship('AdditionalService', backref='listing', lazy=True, cascade='all, delete-orphan')

class AdditionalService(db.Model):
    __tablename__ = 'additional_services'
    
    service_id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.listing_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)

class ListingImage(db.Model):
    __tablename__ = 'listing_images'
    
    image_id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.listing_id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer)

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    booking_id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.listing_id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'confirmed', 'cancelled', 'completed'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Отношения
    listing = db.relationship('Listing', backref='bookings', lazy=True)
    tenant = db.relationship('User', backref='bookings', lazy=True)
    booking_services = db.relationship('BookingService', backref='booking', lazy=True, cascade='all, delete-orphan')

class BookingService(db.Model):
    __tablename__ = 'booking_services'
    
    booking_service_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('additional_services.service_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Отношения
    service = db.relationship('AdditionalService', backref='booking_services', lazy=True) 