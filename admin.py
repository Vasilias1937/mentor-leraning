from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import User, Listing, Booking
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'admin':
            flash('У вас нет прав для доступа к этой странице', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def index():
    users_count = User.query.count()
    listings_count = Listing.query.count()
    bookings_count = Booking.query.count()
    return render_template('admin/index.html',
                         users_count=users_count,
                         listings_count=listings_count,
                         bookings_count=bookings_count)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.filter(User.user_type != 'admin').all()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/users/<int:user_id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_verified = True
    db.session.commit()
    flash('Пользователь успешно верифицирован', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.user_type == 'admin':
        flash('Нельзя удалить администратора', 'error')
        return redirect(url_for('admin.users'))
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь успешно удалён', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/listings')
@login_required
@admin_required
def listings():
    listings = Listing.query.all()
    return render_template('admin/listings.html', listings=listings)

@admin_bp.route('/listings/<int:listing_id>/moderate', methods=['POST'])
@login_required
@admin_required
def moderate_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    action = request.form.get('action')
    
    if action == 'approve':
        listing.is_active = True
        flash('Объявление одобрено', 'success')
    elif action == 'reject':
        listing.is_active = False
        flash('Объявление отклонено', 'success')
    
    db.session.commit()
    return redirect(url_for('admin.listings'))

@admin_bp.route('/bookings')
@login_required
@admin_required
def bookings():
    bookings = Booking.query.all()
    return render_template('admin/bookings.html', bookings=bookings)

@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    # Здесь можно добавить логику для сбора аналитики
    return render_template('admin/analytics.html') 