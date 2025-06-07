from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

from werkzeug.utils import redirect

app = Flask(__name__)

app.secret_key = '&%#hbbfdyuis54*^%#GHF*Y( 6t6t(*^t98'




@app.route('/register', methods=['POST', 'GET'])
def register():

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if request.method == 'POST':


        conn = sqlite3.connect('authentication.db')
        cursor = conn.cursor()

        cursor.execute("SELECT 1 from user where email = ? OR username = ?", (email, username))

        if cursor.fetchone():
            flash('Email or username already exists, try again.', 'warning')

            return redirect(url_for('register'))
        cursor.execute('''INSERT INTO user (username, email, password, role) VALUES (?, ?, ?, ?)''',
                           (username, email, password, 'user'))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/register/admin', methods=['POST', 'GET'])
def admin_register():

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')


    if request.method == 'POST':

        conn = sqlite3.connect('authentication.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*)  FROM user WHERE role = 'admin'")

        admin_count = cursor.fetchone()[0]


        if admin_count >= 1:
            return "An admin already exists. Permission denied."

        else:
            cursor.execute('''INSERT INTO user (username, email, password, role) VALUES (?, ?, ?, ?)''',(username, email, password, 'admin'))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))
    return render_template('admin-signup.html')
@app.route('/login')
def login():


    return render_template('login.html')

@app.route('/forgot-password', methods=['POST', 'GET'])
def forgot_password():

    return render_template('forgot-password.html')


if __name__ == '__main__':
    app.run(debug=True)
