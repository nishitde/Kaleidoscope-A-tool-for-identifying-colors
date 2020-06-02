# Name: Nishit De, E-mail: npd57@drexel.edu
# CS530: DUI Project

from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect
from passlib.hash import pbkdf2_sha256
import os
import sqlite3
from db import Database

app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = b'lkj98t&%$3rhfSwu3D'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Handle the home page
@app.route('/')
def index():
    return render_template('index.html')

# Handle any files that begin "/course" by loading from the course directory
@app.route('/course/<path:path>')
def base_static(path):
    return send_file(os.path.join(app.root_path, '..', 'course', path))

# Handles the Sign-up operation
@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        typed_password = request.form['password']
        if username and typed_password:
            encryptedpassword = pbkdf2_sha256.encrypt(typed_password, rounds=200000, salt_size=16)
            get_db().create_user(username, encryptedpassword)
            return redirect('/')
    return render_template('index.html')

# Handles the Log-In operation
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        typed_password = request.form['password']
        if username and typed_password:
            user = get_db().get_user(username)
            if user:
                if pbkdf2_sha256.verify(typed_password, user['encryptedpassword']):
                    session['user'] = user
                    return redirect('/')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif username and not typed_password:
            message = "Missing password, please try again"
        elif not username and typed_password:
            message = "Missing username, please try again"
    return render_template('index.html', message=message)

# Handles the Log-Out operation
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# Routes to pages depending if 'User' is in session or not
@app.route('/<name>')
def generic(name):
    if 'user' in session:
        return render_template(name + '.html')
    else:
        return render_template(name + '.html')

# Handles the uploading of the title in the Database
@app.route('/form', methods=['GET', 'POST'])
def create_survey():
    if request.method == 'POST':
        title = request.form['title']
        get_db().create_survey(title)
        question1 = request.form['question1']
        question_id1 = request.form['question_no1']
        get_db().create_question(title, question_id1, question1)
        answer1 = request.form['answer1']
        answer1_a = request.form['answer1_a']
        answer1_b = request.form['answer1_b']
        answer1_c = request.form['answer1_c']
        get_db().create_answer(question_id1, answer1)
        get_db().create_answer(question_id1, answer1_a)
        get_db().create_answer(question_id1, answer1_b)
        get_db().create_answer(question_id1, answer1_c)
        question2 = request.form['question2']
        question_id2 = request.form['question_no2']
        get_db().create_question(title, question_id2, question2)
        answer2 = request.form['answer2']
        answer2_a = request.form['answer2_a']
        answer2_b = request.form['answer2_b']
        answer2_c = request.form['answer2_c']
        get_db().create_answer(question_id2, answer2)
        get_db().create_answer(question_id2, answer2_a)
        get_db().create_answer(question_id2, answer2_b)
        get_db().create_answer(question_id2, answer2_c)
        question3 = request.form['question3']
        question_id3 = request.form['question_no3']
        get_db().create_question(title, question_id3, question3)
        answer3 = request.form['answer3']
        answer3_a = request.form['answer3_a']
        answer3_b = request.form['answer3_b']
        answer3_c = request.form['answer3_c']
        get_db().create_answer(question_id3, answer3)
        get_db().create_answer(question_id3, answer3_a)
        get_db().create_answer(question_id3, answer3_b)
        get_db().create_answer(question_id3, answer3_c)
        question4 = request.form['question4']
        question_id4 = request.form['question_no4']
        get_db().create_question(title, question_id4, question4)
        answer4 = request.form['answer4']
        answer4_a = request.form['answer4_a']
        answer4_b = request.form['answer4_b']
        answer4_c = request.form['answer4_c']
        get_db().create_answer(question_id4, answer4)
        get_db().create_answer(question_id4, answer4_a)
        get_db().create_answer(question_id4, answer4_b)
        get_db().create_answer(question_id4, answer4_c)
        question5 = request.form['question5']
        question_id5 = request.form['question_no5']
        get_db().create_question(title, question_id5, question5)
        answer5 = request.form['answer5']
        answer5_a = request.form['answer5_a']
        answer5_b = request.form['answer5_b']
        answer5_c = request.form['answer5_c']
        get_db().create_answer(question_id5, answer5)
        get_db().create_answer(question_id5, answer5_a)
        get_db().create_answer(question_id5, answer5_b)
        get_db().create_answer(question_id5, answer5_c)
    return render_template('generate.html')

# Displaying the Surveys
@app.route('/survey')
def display_survey():
    questions = []
    con = sqlite3.connect('survey.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT title FROM survey")
    rows = cur.fetchall()
    return render_template("survey.html", rows = rows)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
