from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from models import User, Listing
from forms import LoginForm, RegistrationForm
import logging

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            flash('Неверный email или пароль', 'error')
        except Exception as e:
            logging.error(f"Ошибка при входе: {str(e)}")
            flash('Произошла ошибка при попытке входа. Пожалуйста, попробуйте позже.', 'error')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            user_type=form.user_type.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.register'))
    user_listings = []
    if current_user.user_type == 'landlord':
        from models import Listing # Импортируем здесь, чтобы избежать циклической зависимости
        user_listings = Listing.query.filter_by(landlord_id=current_user.user_id, is_active=True).all()
    return render_template('auth/profile.html', user=current_user, listings=user_listings)

@auth_bp.route('/reset_password_request')
def reset_password_request():
    # Это заглушка. Здесь будет логика запроса сброса пароля.
    flash('Функция сброса пароля пока не реализована.', 'info')
    return redirect(url_for('auth.login')) 