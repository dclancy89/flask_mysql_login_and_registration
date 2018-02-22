import md5

from flask import Flask, render_template, request, redirect, session, flash
app = Flask(__name__)
app.secret_key = 'jkfu890342htruo34v7yut8039pthjiopv78t0432-y5t3480wtb342y905n34um20w'

from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app, 'login_and_reguustration_db')

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
	if session.get('id') != None:
		return redirect('/members')

	return render_template('index.html')

@app.route('/members')
def members():
	if session.get('id') == None:
		return redirect('/')

	return render_template('members.html')

@app.route('/register', methods=['post'])
def register():
	session['first_name'] = request.form['first_name']
	session['last_name'] = request.form['last_name']
	session['email'] = request.form['email']
	session['password'] = request.form['password']
	session['confirm_pw'] = request.form['confirm_pw']

	first_name_valid = False
	last_name_valid = False
	email_valid = False
	password_valid = False
	passwords_match = False

	# check if email already exists in db
	query = "SELECT * FROM users WHERE email=:email"
	data = {'email': session['email']}

	result = mysql.query_db(query, data)

	if len(result) != 0:
		flash("User already exists.", 'error')
		return redirect("/")

	# validate first name
	if session['first_name'].isalpha() and len(session['first_name']) > 1:
		first_name_valid = True
	else:
		if not session['first_name'].isalpha():
			flash("First name can only be letters.", 'error')
		if len(session['first_name']) < 2:
			flash("First name must be at least two characters long.", 'error')

	# validate last name
	if session['last_name'].isalpha() and len(session['last_name']) > 1:
		last_name_valid = True
	else:
		if not session['last_name'].isalpha():
			flash("Last name can only be letters.", 'error')
		if len(session['last_name']) < 2:
			flash("Last name must be at least two characters long.", 'error')

	# validate email
	if EMAIL_REGEX.match(session['email']):
		email_valid = True
	else:
		flash('Must submit a valid email address.', 'error')

	# validate password
	if len(session['password']) > 8:
		password_valid = True
	else:
		flash('Password must be at least 8 characters long.', 'error')

	# check if passwords match
	if session['password'] == session['confirm_pw']:
		passwords_match = True
	else:
		flash("Passwords must match.", 'error')


	# if everything is valid, send the new user to the members page
	if first_name_valid and last_name_valid and email_valid and password_valid and passwords_match:
		query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
		data = {
				'first_name': session['first_name'],
				'last_name': session['last_name'],
				'email': session['email'],
				'password': md5.new(session['password']).hexdigest()
		}

		mysql.query_db(query, data)

		query = "SELECT * FROM users WHERE first_name=:first_name AND last_name=:last_name AND email=:email"
		data = {
				'first_name': session['first_name'],
				'last_name': session['last_name'],
				'email': session['email']
		}
		user = mysql.query_db(query, data)
		session.clear()
		session['id'] = user[0]['id']
		session['first_name'] = user[0]['first_name']
		return redirect('/members')
	# if not valid, try again
	else:
		return redirect('/')


@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']

	query = "SELECT * FROM users WHERE email=:email AND password=:password"
	data = {
			'email': email,
			'password': md5.new(password).hexdigest()
	}

	user = mysql.query_db(query, data)

	if len(user) != 0:
		session['id'] = user[0]['id']
		session['first_name'] = user[0]['first_name']
		return redirect('/members')
	else:
		flash("Incorrect email and password combination", 'error')
		return redirect('/')


@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

app.run(debug=True)