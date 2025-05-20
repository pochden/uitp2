from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
import json
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)

DB_FILE = r'D:\UITPproject\users.json'
TOURS_FILE = r'D:\UITPproject\tours.json'

os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
os.makedirs(os.path.dirname(TOURS_FILE), exist_ok=True)

def load_users():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            app.logger.error(f"Ошибка чтения users.json: {e}")
            return {}
    return {}

def save_users(users):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        app.logger.error(f"Ошибка записи users.json: {e}")

def load_tours():
    if os.path.exists(TOURS_FILE):
        try:
            with open(TOURS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            app.logger.error(f"Ошибка чтения tours.json: {e}")
            return []
    return []

def save_tours(tours):
    try:
        with open(TOURS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tours, f, ensure_ascii=False, indent=2)
    except Exception as e:
        app.logger.error(f"Ошибка записи tours.json: {e}")

@app.route('/submit_tour', methods=['POST'])
def submit_tour():
    if 'username' not in session:
        return redirect(url_for('profile'))
    tour_data = {
        'name': request.form['name'],
        'phone': request.form['phone'],
        'email': request.form.get('email', ''),
        'date': request.form['date'],
        'user': session['username'],
        'paid': 'Нет'
    }
    tours = load_tours()
    tours.append(tour_data)
    save_tours(tours)
    return redirect(url_for('tours'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/departments')
def departments():
    return render_template('departments.html')

@app.route('/guides')
def guides():
    return render_template('guides.html')

@app.route('/places')
def places():
    return render_template('places.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/tours')
def tours():
    if 'username' not in session:
        return redirect(url_for('profile'))
    return render_template('tours.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    if request.method == 'POST':
        if 'register' in request.form:
            username = request.form['username']
            password = request.form['password']
            users = load_users()
            if username in users:
                return render_template('profile.html', error='Имя пользователя уже занято')
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            users[username] = hashed_password
            save_users(users)
            session['username'] = username
            return redirect(url_for('profile'))
        elif 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            users = load_users()
            if username in users and bcrypt.check_password_hash(users[username], password):
                session['username'] = username
                return redirect(url_for('profile'))
            else:
                return render_template('profile.html', error='Неверное имя пользователя или пароль')
    return render_template('profile.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('profile'))

@app.route('/admin')
def admin():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('profile'))
    users = load_users()
    tours = load_tours()
    return render_template('admin.html', users=users, tours=tours)

@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('profile'))
    username = request.form['username']
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
    return redirect(url_for('admin'))

@app.route('/add_user', methods=['POST'])
def add_user():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('profile'))
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    if username in users:
        return redirect(url_for('admin'))
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users[username] = hashed_password
    save_users(users)
    return redirect(url_for('admin'))

@app.route('/update_payment', methods=['POST'])
def update_payment():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('profile'))
    tour_index = int(request.form['tour_index'])
    paid = request.form['paid']
    tours = load_tours()
    if 0 <= tour_index < len(tours):
        tours[tour_index]['paid'] = paid
        save_tours(tours)
    return redirect(url_for('admin'))

# Исправленная функция photos()
@app.route('/photos')
def photos():
    photos_dir = os.path.join(app.static_folder, 'photos')
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)
    photos = [f for f in os.listdir(photos_dir) if os.path.isfile(os.path.join(photos_dir, f))]
    return render_template('photos.html', photos=photos)

def create_admin():
    users = load_users()
    if 'admin' not in users:
        hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
        users['admin'] = hashed_password
        save_users(users)

create_admin()

if __name__ == '__main__':
    app.run(debug=True)