from flask import Flask, render_template, request, redirect, session, flash
app = Flask(__name__)
app.secret_key = 'jkfu890342htruo34v7yut8039pthjiopv78t0432-y5t3480wtb342y905n34um20w'

from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app, 'login_and_registration_db')

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
	email_valid = True
	password_valid = True
	passwords_match = True

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

	if first_name_valid and last_name_valid and email_valid and password_valid and passwords_match:
		session['id'] = 1
		return redirect('/members')
	else:
		return redirect('/')


@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

app.run(debug=True)