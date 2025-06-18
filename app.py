from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Инициализация расширений
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.register'

from models import User, Listing

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Импорт и регистрация blueprints
from auth import auth_bp
from listings import listings_bp
from admin import admin_bp
from bookings import bookings_bp

app.register_blueprint(auth_bp)
app.register_blueprint(listings_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(bookings_bp)

@app.route('/')
def index():
    sort = request.args.get('sort', 'date_desc')
    room_type = request.args.get('room_type')
    query = Listing.query.filter_by(is_active=True)
    if room_type:
        query = query.filter(Listing.room_type == room_type)
    if sort == 'price_asc':
        query = query.order_by(Listing.base_price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Listing.base_price.desc())
    elif sort == 'area_asc':
        query = query.order_by(Listing.area_sqm.asc())
    elif sort == 'area_desc':
        query = query.order_by(Listing.area_sqm.desc())
    else:  # date_desc
        query = query.order_by(Listing.created_at.desc())
    listings = query.all()
    return render_template('index.html', listings=listings)

if __name__ == '__main__':
    app.run(debug=True) 