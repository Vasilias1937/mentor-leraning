from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, make_response
from flask_login import login_required, current_user
from app import db, allowed_file
from models import Listing, ListingImage, AdditionalService
from forms import ListingForm
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import time
import logging
from weasyprint import HTML

listings_bp = Blueprint('listings', __name__)

@listings_bp.route('/listings')
def index():
    listings = Listing.query.filter_by(is_active=True).all()
    return render_template('listings/index.html', listings=listings)

@listings_bp.route('/listings/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.user_type != 'landlord':
        flash('Для размещения объявления авторизируйтесь как арендодатель.', 'error')
        return redirect(url_for('listings.index'))
        
    form = ListingForm()
    if form.validate_on_submit():
        try:
            listing = Listing(
                title=form.title.data,
                description=form.description.data,
                address=form.address.data,
                city=form.city.data,
                region=form.region.data,
                country=form.country.data,
                postal_code=form.postal_code.data,
                base_price=form.base_price.data,
                area_sqm=form.area_sqm.data,
                min_lease_period_months=form.min_lease_period_months.data,
                landlord_id=current_user.user_id,
                room_type=form.room_type.data
            )
            db.session.add(listing)
            db.session.flush()  # Получаем ID объявления

            # Логируем, что пришло в images
            current_app.logger.info(f"form.images.data: {form.images.data}")

            # Обработка загруженных изображений
            if form.images.data:
                files = form.images.data if isinstance(form.images.data, list) else [form.images.data]
                for file in files:
                    current_app.logger.info(f"Обрабатывается файл: {getattr(file, 'filename', str(file))}")
                    if file and file.filename and allowed_file(file.filename):
                        try:
                            filename = secure_filename(file.filename)
                            unique_filename = f"{listing.listing_id}_{int(time.time())}_{filename}"
                            upload_folder = current_app.config['UPLOAD_FOLDER']
                            os.makedirs(upload_folder, exist_ok=True)
                            file_path = os.path.join(upload_folder, unique_filename)
                            current_app.logger.info(f"Saving file to: {file_path}")
                            file.save(file_path)
                            image = ListingImage(
                                listing_id=listing.listing_id,
                                image_url=unique_filename
                            )
                            db.session.add(image)
                            current_app.logger.info(f"Image saved successfully: {unique_filename}")
                        except Exception as e:
                            current_app.logger.error(f"Error saving image: {str(e)}")
                            flash(f'Ошибка при сохранении изображения: {str(e)}', 'error')

            db.session.commit()
            flash('Объявление успешно создано!', 'success')
            return redirect(url_for('listings.view', listing_id=listing.listing_id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating listing: {str(e)}")
            flash(f'Произошла ошибка при создании объявления: {str(e)}', 'error')
            
    return render_template('listings/create.html', form=form)

@listings_bp.route('/listings/<int:listing_id>')
def view(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template('listings/view.html', listing=listing)

@listings_bp.route('/listings/<int:listing_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    if current_user.user_id != listing.landlord_id:
        flash('У вас нет прав на редактирование этого объявления', 'error')
        return redirect(url_for('listings.view', listing_id=listing_id))
    
    form = ListingForm(obj=listing)
    if form.validate_on_submit():
        listing.title = form.title.data
        listing.description = form.description.data
        listing.address = form.address.data
        listing.city = form.city.data
        listing.region = form.region.data
        listing.country = form.country.data
        listing.postal_code = form.postal_code.data
        listing.base_price = form.base_price.data
        listing.area_sqm = form.area_sqm.data
        listing.min_lease_period_months = form.min_lease_period_months.data
        listing.updated_at = datetime.utcnow()
        listing.room_type = form.room_type.data
        
        db.session.commit()
        flash('Объявление успешно обновлено', 'success')
        return redirect(url_for('listings.view', listing_id=listing_id))
    
    return render_template('listings/edit.html', form=form, listing=listing)

@listings_bp.route('/listings/<int:listing_id>/delete', methods=['POST'])
@login_required
def delete(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    if current_user.user_id != listing.landlord_id:
        flash('У вас нет прав на удаление этого объявления', 'error')
        return redirect(url_for('listings.view', listing_id=listing_id))
    
    listing.is_active = False
    db.session.commit()
    flash('Объявление успешно удалено', 'success')
    return redirect(url_for('listings.index'))

@listings_bp.route('/listings/<int:listing_id>/download')
def download(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    rendered = render_template('listings/view.html', listing=listing, pdf_mode=True)
    pdf = HTML(string=rendered, base_url=request.base_url).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=listing_{listing_id}.pdf'
    return response 