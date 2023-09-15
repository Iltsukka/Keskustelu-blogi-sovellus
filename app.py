from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.secret_key = getenv('SECRET_KEY')
db = SQLAlchemy(app)

#tämä on vain testi poistan myöhemmin
@app.route('/testi')
def testi():
    result = db.session.execute(text('SELECT content FROM messages'))
    messages = result.fetchall()
    return render_template('testi.html', count=len(messages), messages=messages)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    sql = text('SELECT username, password FROM users WHERE username=:username')
    result = db.session.execute(sql, {"username":username})
    user_info = result.fetchone()
    if user_info:
        hash = user_info.password
        if check_password_hash(hash, password):
            session['username'] = username
            return redirect('/')
        else:
            return 'wrong password'
    else:
        return 'invalid username'

@app.route('/create_form')
def createform():
    return render_template('create.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    hash = generate_password_hash(password)
    sql = text('INSERT INTO users (username, password) VALUES (:username, :password)')
    db.session.execute(sql, {'username':username, 'password':hash})
    db.session.commit()
    return 'success?'

@app.route('/log_out', methods=['POST'])
def log_out():
    del session['username']
    return redirect('/')
    
    