from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, DecimalField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange
from flask_wtf.file import FileField, FileAllowed
from datetime import date

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, message='Пароль должен быть не менее 8 символов')
    ])
    password2 = PasswordField('Подтвердите пароль', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать')
    ])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    user_type = SelectField('Тип пользователя', choices=[
        ('tenant', 'Арендатор'),
        ('landlord', 'Арендодатель')
    ], validators=[DataRequired()])

class ListingForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    region = StringField('Область', validators=[DataRequired()])
    country = StringField('Страна', validators=[DataRequired()])
    postal_code = StringField('Почтовый индекс', validators=[DataRequired()])
    base_price = DecimalField('Базовая цена', validators=[
        DataRequired(),
        NumberRange(min=0, message='Цена должна быть положительной')
    ])
    area_sqm = DecimalField('Площадь (м²)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Площадь должна быть положительной')
    ])
    min_lease_period_months = IntegerField('Минимальный срок аренды (месяцев)', validators=[
        DataRequired(),
        NumberRange(min=1, message='Срок должен быть не менее 1 месяца')
    ])
    room_type = SelectField(
        'Тип помещения',
        choices=[
            ('freezer', 'Морозильная камера'),
            ('warehouse', 'Складское помещение'),
            ('production', 'Производственное помещение')
        ],
        validators=[DataRequired()]
    )
    images = FileField('Изображения объявления', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Только изображения!')
    ])

class BookingForm(FlaskForm):
    start_date = DateField('Дата начала', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('Дата окончания', validators=[DataRequired()], format='%Y-%m-%d')
    additional_services = SelectField('Дополнительные услуги', coerce=int, validators=[Optional()]) 