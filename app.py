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
    sql = text('SELECT * FROM blogs')
    result = db.session.execute(sql)
    blogs = result.fetchall()
    if blogs:
        return render_template('index.html', blogs=blogs)
    
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
            return render_template('error.html', error_message='Invalid username or password')
    else:
        return render_template('error.html', error_message='Invalid username or password')

@app.route('/create_form')
def createform():
    return render_template('create.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    if password == '' or username == '':
        return render_template('error.html', error_message='Password and username cannot be empty')
    if password != password2:
        return render_template('error.html', error_message='passwords must match')
    hash = generate_password_hash(password)
    sql = text('INSERT INTO users (username, password) VALUES (:username, :password)')
    try:
        db.session.execute(sql, {'username':username, 'password':hash})
        db.session.commit()
        session['username'] = username
        return redirect('/')
    except:
        return render_template('error.html', error_message='Username already in use')

@app.route('/log_out', methods=['POST'])
def log_out():
    del session['username']
    return redirect('/')

@app.route('/blogform', methods=['POST'])
def blogform():
    return render_template('newblog.html')

@app.route('/create_blog', methods=['POST'])
def create_blog():
    topic = request.form['topic']
    if len(topic) < 20 or len(topic) > 400:
        return render_template('error.html', error_message='Post must be between 20 and 400 characters long')
    if topic == '':
        return render_template('error.html', error_message='post cannot be empty')
    username = session['username']
    sql = text("INSERT INTO blogs (topic, username, time_of, visible) VALUES (:topic, :username, NOW(), TRUE)")
    if username:
        db.session.execute(sql, {"topic":topic, "username":username})
        db.session.commit()
        return redirect('/')
    else:
        return render_template('error.html', error_message='Did not succesfully create a blog')

@app.route('/visit/<int:id>')
def visit(id):
    sql = text('SELECT * FROM blogs WHERE id=:id')
    result = db.session.execute(sql, {"id":id})
    blog = result.fetchone()
    sql2 = text('SELECT * FROM comments WHERE :id=blog_id')
    result2 = db.session.execute(sql2, {"id":id})
    comments = result2.fetchall()
    return render_template('comments.html', blog=blog, comments=comments)

@app.route('/add_comment/<int:id>', methods=['POST'])
def add_comment(id):
    content = request.form['content']
    if content == '':
        return render_template('error.html', error_message='empty comments are not allowed')
    if len(content) < 10 or len(content) > 400:
        return render_template('error.html', error_message='Comments must be between 10 and 400 characters long!')
    username = session['username']
    if username:
        blog_id = id
        sql = text('INSERT INTO comments (content, date_of, username, blog_id) VALUES (:content, NOW(), :username, :blog_id)')
        db.session.execute(sql, {"content":content, "username":username, "blog_id":blog_id})
        db.session.commit()
        return redirect(f"/visit/{id}")
    else:
        return render_template('error.html', error_message='Only logged in users can send comments')
    
@app.route('/user_posts')
def user_posts():
    username = session['username']
    if username:
        sql = text('SELECT * FROM blogs WHERE username=:username')
        result = db.session.execute(sql, {"username":username})
        blogs = result.fetchall()
        return render_template('user_posts.html', blogs=blogs)
    else:
        return render_template('error.html', error_message='Action only allowed for users logged in')

@app.route('/delete_blog/<int:id>', methods=['POST'])
def delete_blog(id):
    try:
        sql = text('UPDATE blogs SET visible=FALSE WHERE id=:id')
        db.session.execute(sql, {'id':id})
        db.session.commit()
        return redirect('/user_posts')
    except:
        return render_template('error.html', error_message='Blog could not be deleted')

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    sql = text('SELECT * FROM blogs WHERE id=:id')
    result = db.session.execute(sql, {"id":id})
    blog = result.fetchone()
    return render_template('edit.html', blog=blog)

@app.route('/change_topic/<int:id>', methods=['POST'])
def change_topic(id):
    topic = request.form['newtopic']
    if len(topic) <20 or len(topic)> 400:
        return render_template('error.html', error_message='Post must be between 20 and 400 characters long')
    try:
        sql = text('UPDATE blogs SET topic=:topic WHERE id=:id')
        db.session.execute(sql, {"topic":topic, "id":id})
        db.session.commit()
        return redirect('/user_posts')
    except:
        return render_template('error.html', error_message='Something went wrong trying to edit blog topic')
    
@app.route('/polls')
def polls():
    sql = text('SELECT id, questions, created_at, username FROM polls ORDER BY id')
    result = db.session.execute(sql)
    polls = result.fetchall()
    return render_template('polls.html', polls=polls)

@app.route('/newpoll')
def new_poll():
    return render_template('new_poll.html')

@app.route('/create_poll', methods=['POST'])
def create_poll():
    try:
        username = session['username']
        if not username:
            return render_template('error.html', error_message='This action is for logged in users only')
        question = request.form['question']
        sql = text('INSERT INTO polls (questions, created_at, username) VALUES (:question, NOW(), :username) RETURNING id')
        result = db.session.execute(sql, {"question":question, "username":username})
        question_id = result.fetchone()[0]
        options = request.form.getlist('option')
        for option in options:
            if option != '':
                sql2 = text('INSERT INTO options (poll_id, option) VALUES (:question_id, :option)')
                db.session.execute(sql2, {"question_id":question_id, "option":option})
        db.session.commit()
        return redirect('/polls')
    except:
        return render_template('error.html', error_message='Something went wrong creating the poll')
    
@app.route('/answer_poll/<int:id>')
def answer_poll(id):
    sql = text('SELECT questions, created_at, username FROM polls WHERE id=:id')
    result = db.session.execute(sql, {"id":id})
    question = result.fetchone()
    sql2 = text('SELECT id, option FROM options WHERE poll_id=:id')
    result2 = db.session.execute(sql2, {"id":id})
    options = result2.fetchall()
    return render_template('answer_poll.html', question=question, options=options)

@app.route('/poll_answers', methods=['POST'])
def poll_answers():
    if 'input' in request.form:
        option_id = request.form['input']
        sql = text('INSERT INTO answers (options_id, made_at) VALUES (:option_id, NOW())')
        db.session.execute(sql, {"option_id":option_id})
        db.session.commit()
        return redirect('/polls')


