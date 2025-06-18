from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Listing, Booking, BookingService, AdditionalService, User
from forms import BookingForm
from datetime import datetime, date, timedelta
from sqlalchemy import and_, or_

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings')
@login_required
def index():
    """Список бронирований пользователя"""
    if current_user.user_type == 'tenant':
        # Для арендаторов показываем их бронирования
        bookings = Booking.query.filter_by(tenant_id=current_user.user_id).order_by(Booking.created_at.desc()).all()
    else:
        # Для арендодателей показываем бронирования их помещений
        bookings = Booking.query.join(Listing).filter(
            Listing.landlord_id == current_user.user_id
        ).order_by(Booking.created_at.desc()).all()
    
    return render_template('bookings/index.html', bookings=bookings)

@bookings_bp.route('/listings/<int:listing_id>/book', methods=['GET', 'POST'])
@login_required
def create(listing_id):
    """Создание нового бронирования"""
    if current_user.user_type != 'tenant':
        flash('Только арендаторы могут бронировать помещения', 'error')
        return redirect(url_for('listings.view', listing_id=listing_id))
    
    listing = Listing.query.get_or_404(listing_id)
    
    # Проверяем, что помещение активно
    if not listing.is_active:
        flash('Это помещение недоступно для бронирования', 'error')
        return redirect(url_for('listings.view', listing_id=listing_id))
    
    form = BookingForm()
    
    # Получаем доступные дополнительные услуги
    additional_services = AdditionalService.query.filter_by(listing_id=listing_id).all()
    form.additional_services.choices = [(0, 'Без дополнительных услуг')] + [(s.service_id, f"{s.name} - {s.price} ₽") for s in additional_services]
    
    if form.validate_on_submit():
        try:
            start_date = form.start_date.data
            end_date = form.end_date.data
            
            # Проверяем минимальный срок аренды
            min_days = listing.min_lease_period_months * 30  # Примерно
            booking_days = (end_date - start_date).days
            if booking_days < min_days:
                flash(f'Минимальный срок аренды составляет {listing.min_lease_period_months} месяцев ({min_days} дней)', 'error')
                return render_template('bookings/create.html', form=form, listing=listing, additional_services=additional_services)
            
            # Проверяем, что даты не в прошлом
            if start_date < date.today():
                flash('Дата начала не может быть в прошлом', 'error')
                return render_template('bookings/create.html', form=form, listing=listing, additional_services=additional_services)
            
            # Проверяем, что дата окончания после даты начала
            if end_date <= start_date:
                flash('Дата окончания должна быть после даты начала', 'error')
                return render_template('bookings/create.html', form=form, listing=listing, additional_services=additional_services)
            
            # Проверяем доступность дат
            conflicting_bookings = Booking.query.filter(
                and_(
                    Booking.listing_id == listing_id,
                    Booking.status.in_(['pending', 'confirmed']),
                    or_(
                        and_(Booking.start_date <= start_date, Booking.end_date > start_date),
                        and_(Booking.start_date < end_date, Booking.end_date >= end_date),
                        and_(Booking.start_date >= start_date, Booking.end_date <= end_date)
                    )
                )
            ).first()
            
            if conflicting_bookings:
                flash('Выбранные даты уже забронированы', 'error')
                return render_template('bookings/create.html', form=form, listing=listing, additional_services=additional_services)
            
            # Рассчитываем общую стоимость
            months = (end_date - start_date).days / 30.44  # Среднее количество дней в месяце
            base_price = float(listing.base_price) * months
            
            # Добавляем стоимость дополнительных услуг
            additional_cost = 0
            if form.additional_services.data and form.additional_services.data != 0:
                service = AdditionalService.query.get(form.additional_services.data)
                if service:
                    additional_cost = float(service.price) * months
            
            total_price = base_price + additional_cost
            
            # Создаем бронирование
            booking = Booking(
                listing_id=listing_id,
                tenant_id=current_user.user_id,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status='pending'
            )
            db.session.add(booking)
            db.session.flush()  # Получаем ID бронирования
            
            # Добавляем дополнительные услуги
            if form.additional_services.data and form.additional_services.data != 0:
                service = AdditionalService.query.get(form.additional_services.data)
                if service:
                    booking_service = BookingService(
                        booking_id=booking.booking_id,
                        service_id=service.service_id,
                        quantity=1,
                        total_price=additional_cost
                    )
                    db.session.add(booking_service)
            
            db.session.commit()
            flash('Бронирование успешно создано!', 'success')
            return redirect(url_for('bookings.view', booking_id=booking.booking_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Произошла ошибка при создании бронирования: {str(e)}', 'error')
    
    return render_template('bookings/create.html', form=form, listing=listing, additional_services=additional_services)

@bookings_bp.route('/bookings/<int:booking_id>')
@login_required
def view(booking_id):
    """Просмотр бронирования"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Проверяем права доступа
    if current_user.user_type == 'tenant' and booking.tenant_id != current_user.user_id:
        flash('У вас нет прав на просмотр этого бронирования', 'error')
        return redirect(url_for('bookings.index'))
    
    if current_user.user_type == 'landlord' and booking.listing.landlord_id != current_user.user_id:
        flash('У вас нет прав на просмотр этого бронирования', 'error')
        return redirect(url_for('bookings.index'))
    
    return render_template('bookings/view.html', booking=booking)

@bookings_bp.route('/bookings/<int:booking_id>/confirm', methods=['POST'])
@login_required
def confirm(booking_id):
    """Подтверждение бронирования арендодателем"""
    booking = Booking.query.get_or_404(booking_id)
    
    if current_user.user_type != 'landlord' or booking.listing.landlord_id != current_user.user_id:
        flash('У вас нет прав на подтверждение этого бронирования', 'error')
        return redirect(url_for('bookings.view', booking_id=booking_id))
    
    if booking.status != 'pending':
        flash('Это бронирование уже обработано', 'error')
        return redirect(url_for('bookings.view', booking_id=booking_id))
    
    booking.status = 'confirmed'
    booking.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Бронирование подтверждено', 'success')
    return redirect(url_for('bookings.view', booking_id=booking_id))

@bookings_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel(booking_id):
    """Отмена бронирования"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Проверяем права доступа
    can_cancel = False
    if current_user.user_type == 'tenant' and booking.tenant_id == current_user.user_id:
        can_cancel = True
    elif current_user.user_type == 'landlord' and booking.listing.landlord_id == current_user.user_id:
        can_cancel = True
    
    if not can_cancel:
        flash('У вас нет прав на отмену этого бронирования', 'error')
        return redirect(url_for('bookings.view', booking_id=booking_id))
    
    if booking.status not in ['pending', 'confirmed']:
        flash('Это бронирование нельзя отменить', 'error')
        return redirect(url_for('bookings.view', booking_id=booking_id))
    
    booking.status = 'cancelled'
    booking.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Бронирование отменено', 'success')
    return redirect(url_for('bookings.view', booking_id=booking_id))

@bookings_bp.route('/listings/<int:listing_id>/availability')
def availability(listing_id):
    """API для получения доступных дат"""
    listing = Listing.query.get_or_404(listing_id)
    
    # Получаем все активные бронирования для этого помещения
    bookings = Booking.query.filter(
        and_(
            Booking.listing_id == listing_id,
            Booking.status.in_(['pending', 'confirmed'])
        )
    ).all()
    
    # Формируем список забронированных дат
    booked_dates = []
    for booking in bookings:
        current_date = booking.start_date
        while current_date < booking.end_date:
            booked_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
    
    return jsonify({
        'booked_dates': booked_dates,
        'min_lease_period_months': listing.min_lease_period_months
    }) 