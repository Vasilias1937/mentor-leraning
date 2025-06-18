from flask import current_app
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    # Отправка email в отдельном потоке
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        'Сброс пароля - СкладПРО',
        recipients=[user.email],
        text_body=f'''Для сброса пароля перейдите по следующей ссылке:
{url_for('auth.reset_password', token=token, _external=True)}

Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.
''',
        html_body=f'''
<p>Для сброса пароля перейдите по следующей ссылке:</p>
<p><a href="{url_for('auth.reset_password', token=token, _external=True)}">Сбросить пароль</a></p>
<p>Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.</p>
'''
    )

def send_booking_confirmation_email(booking):
    send_email(
        'Подтверждение бронирования - СкладПРО',
        recipients=[booking.tenant.email],
        text_body=f'''Ваше бронирование подтверждено!

Детали бронирования:
Помещение: {booking.listing.title}
Адрес: {booking.listing.address}
Дата начала: {booking.start_date}
Дата окончания: {booking.end_date}
Общая стоимость: {booking.total_price} руб.

Спасибо за использование нашего сервиса!
''',
        html_body=f'''
<h2>Ваше бронирование подтверждено!</h2>
<p><strong>Детали бронирования:</strong></p>
<ul>
    <li>Помещение: {booking.listing.title}</li>
    <li>Адрес: {booking.listing.address}</li>
    <li>Дата начала: {booking.start_date}</li>
    <li>Дата окончания: {booking.end_date}</li>
    <li>Общая стоимость: {booking.total_price} руб.</li>
</ul>
<p>Спасибо за использование нашего сервиса!</p>
'''
    )

def send_booking_notification_to_landlord(booking):
    send_email(
        'Новое бронирование - СкладПРО',
        recipients=[booking.listing.landlord.email],
        text_body=f'''Получено новое бронирование!

Детали бронирования:
Помещение: {booking.listing.title}
Адрес: {booking.listing.address}
Арендатор: {booking.tenant.first_name} {booking.tenant.last_name}
Дата начала: {booking.start_date}
Дата окончания: {booking.end_date}
Общая стоимость: {booking.total_price} руб.

Пожалуйста, подтвердите или отклоните бронирование в личном кабинете.
''',
        html_body=f'''
<h2>Получено новое бронирование!</h2>
<p><strong>Детали бронирования:</strong></p>
<ul>
    <li>Помещение: {booking.listing.title}</li>
    <li>Адрес: {booking.listing.address}</li>
    <li>Арендатор: {booking.tenant.first_name} {booking.tenant.last_name}</li>
    <li>Дата начала: {booking.start_date}</li>
    <li>Дата окончания: {booking.end_date}</li>
    <li>Общая стоимость: {booking.total_price} руб.</li>
</ul>
<p>Пожалуйста, подтвердите или отклоните бронирование в личном кабинете.</p>
'''
    ) 