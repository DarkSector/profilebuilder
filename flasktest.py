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

try:
	c = Connection(pymongoconfig.MONGO_HOST, pymongoconfig.MONGO_PORT)
	dbobj = c[pymongoconfig.MONGO_DATABASE]
except pymongo.errors.AutoReconnect:
	unfortunate = True
else:
	unfortunate = False


#class newProfileBuilderForm(Form):
#	"""Function used to create custom fields"""
#	profileName = TextField('Name of the profile',validators=[Required()])
#	typeProfile = SelectField(u'Type of Technology',
#	choices=[('None','Click to select'),
#			('roof','Roofing'),
#			('wall','Walling'),
#			('found','Foundation'),
#			('misc', 'Miscellaneous')])
#	remarks = TextAreaField('Starting remarks if any')
#	submit = SubmitField('Submit Information')
	
#class loginForm(Form):
#	"""docstring for loginForm"""
#	username = TextField('Your username', validators=[Required()])
#	password = PasswordField('Your Password', validators=[Required()])
#	login = SubmitField('Login')

	
@app.route('/')
def show_profiles():
	"""docstring for show_profiles"""
	if not session.logged_in:
		return redirect(url_for('login'))
	else:
		return render_template('index.html')
	
@app.route('/add',methods=["GET","POST"])
def add_profile():
	"""Add a new profile"""
	#profileform = newProfileBuilderForm(request.form)
	#if profileform.validate_on_submit():

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
	#if loginform.validate_on_submit():
		
	#if request.method == "POST":	
	#	flash('you were logged in')
	#	return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
	"""docstring for logout"""
	session.pop('logged_in', None)
	flash('logged out')
	return redirect(url_for('show_profiles'))
	
if __name__ == "__main__":
	app.run()