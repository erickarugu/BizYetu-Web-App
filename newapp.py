from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from flask import g
import sqlite3

DATABASE = 'userdb.db'

app = Flask(__name__)

@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('home.html')
	else:
		return "Hello Boss!"

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/do_login', methods=['POST'])
def do_login():
	if request.form['password'] == 'password' and request.form['username'] == 'admin':
		return render_template('welcome.html')
	else:
		flash('wrong password!')
		return home()

@app.route('/signup')
def sign_up():
	return render_template('signup.html')

@app.route('/do_sign_up')
def do_sign_up():
	return home()

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=4000)