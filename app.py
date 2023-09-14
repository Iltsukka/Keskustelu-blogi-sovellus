from flask import Flask
from flask import redirect, render_template, request
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
db = SQLAlchemy(app)

#tämä on vain testi poistan myöhemmin
@app.route('/testi')
def index():
    result = db.session.execute(text('SELECT content FROM messages'))
    messages = result.fetchall()
    return render_template('testi.html', count=len(messages), messages=messages)

@app.route('/')
def login():
    return render_template('login.html')