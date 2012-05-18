#!/usr/bin/python
"""
	Rural Housing Knowledge Networks - Database builder
	
	Author: Pronoy Chopra
	IIT Delhi
	
"""

from __future__ import with_statement

import pymongo
from pymongo import Connection
import pymongoconfig
from flask import Flask, request, session, redirect, url_for, abort, \
     render_template, flash
from flask.ext.bcrypt import bcrypt, generate_password_hash, check_password_hash
from flask.ext.wtf import Form, TextField, TextAreaField, \
	 PasswordField, SubmitField, Required, SelectField, ValidationError, \
	 RadioField

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

temp_admin = 'rhknadmin123'
temp_auth = 'clearancehash1'
db_exists = False
user_coll_exists = False

#check if the database exists
#then check if user base exists

conn = Connection(pymongoconfig.MONGO_HOST, pymongoconfig.MONGO_PORT)
dbobj = conn[pymongoconfig.MONGO_DATABASE]
users = dbobj['accesslist']
profiles = dbobj['profiles']

"""
try:
	conn = Connection(pymongoconfig.MONGO_HOST, pymongoconfig.MONGO_PORT)
	dbobj = conn[pymongoconfig.MONGO_DATABASE]
except pymongo.errors.AutoReconnect:
	unfortunate = True
else:
	unfortunate = False
	for i in conn.database_names():
		if i == pymongoconfig.MONGO_DATABASE:
			db_exists = True
			#check if userbase exists
			for l in dbobj.collection_names():
				if l == 'users':
					user_coll_exists = True
					break
			break
"""

@app.route('/')
def show_profiles():
	"""docstring for show_profiles"""
	#if not session.logged_in:
	#	return redirect(url_for('login'))
	#else:
	#	return render_template('index.html')
	return render_template('index.html')
	
@app.route('/add',methods=["GET","POST"])
def add_profile():
	"""Add a new profile"""
	if request.method == "POST":
		name = request.form['title']
		unique = request.form['unique']
		_type = request.form['profiletype']
		profile = {'title':name, 'uniqute': unique, 'profiletype' : _type }
		checkifAdded = profiles.insert(profile)
		if checkifAdded:
			#proceed to editing
			#return redirect(url_for(''))
			print "added yes okay"
			print checkifAdded
			pass
		else:
			flash("Not added")
			print "not added"
		#print name, unique, _type
	return render_template('add.html')
	
@app.route('/edit')
def edit_404():
	flash('Please select the profile you want to edit')
	return redirect(url_for('show_profiles'))

@app.route('/edit/<profilename>',methods=["GET","POST"])
def edit_profile(profilename):
	"""docstring for edit_profile"""
	return	render_template('edit.html')

@app.route('/register')	
def register():
	"""docstring for register"""
	return render_template('register.html')
	
	
@app.route('/login', methods=["GET","POST"])
def login():
	"""docstring for login"""
	#loginform = loginForm(request.form)
	error = None
	if request.method == "POST":
		accuser = request.form['username']
		check_user = users.find_one({'username': accuser})
		print check_user
		print users.find_one()
		if check_user:
			#now check for password
			accpass = request.form['password']
			
			#prepasshash = 
			check_pass = check_password_hash(check_user['password'],accpass)
			if check_pass:
				session['logged_in'] = True
				return redirect(url_for('show_profiles'))
			else:
				print "PASSWORD CHECK FAILED"
				
		else:
			print "USERNAME", accuser ,"DOESN'T EXIST"
	return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
	"""docstring for logout"""
	session.pop('logged_in', None)
	flash('logged out')
	return redirect(url_for('show_profiles'))
	
if __name__ == "__main__":
	app.run()