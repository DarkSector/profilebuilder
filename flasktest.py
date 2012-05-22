#!/usr/bin/python
"""
	Rural Housing Knowledge Networks - Database builder	
	Author: Pronoy Chopra
	IIT Delhi
	
"""

from __future__ import with_statement

import os
import pymongo
from pymongo import Connection
from bson.objectid import ObjectId
import pymongoconfig
from flask import Flask, request, session, redirect, url_for, abort, \
     render_template, flash, g
from flask.ext.bcrypt import bcrypt, generate_password_hash, check_password_hash
import flask_sijax

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

path = os.path.join('.',os.path.dirname(__file__), '../')

app.config['SIJAX_STATIC_PATH'] = os.path.join('.',os.path.dirname(__file__), 'static/js/sijax')

#initialize flask_sijax
flask_sijax.Sijax(app)

conn = Connection(pymongoconfig.MONGO_HOST, pymongoconfig.MONGO_PORT)e

dbobj = conn[pymongoconfig.MONGO_DATABASE]
users = dbobj['accesslist']
profiles = dbobj['profiles']

#@app.route('/',methods=["POST","GET"])
#def show_profiles():
#	allprofiles = profiles.find()
#	return render_template('index.html',profiles=allprofiles)
	
@flask_sijax.route(app,'/')
def show_profiles():
	def delete_profile(obj_response, object_id):
		profiles.remove(ObjectId(object_id))

	if g.sijax.is_sijax_request:
		g.sijax.register_callback('delete_this',delete_profile)
		return g.sijax.process_request()
		
	allprofiles = profiles.find()
	return render_template('index.html', profiles=allprofiles)
	
	
@app.route('/add',methods=["GET","POST"])
def add_profile():
	"""Add a new profile"""
	if request.method == "POST":
		name = request.form['title']
		unique = request.form['unique']
		_type = request.form['profiletype']
		profile = {'title':name, 'unique': unique, 'profiletype' : _type }
		checkifAdded = profiles.insert(profile)
		if checkifAdded:
			return redirect(url_for('show_profiles'))
		else:
			flash("Not added, please try again")
	return render_template('add.html')
	
@app.route('/edit')
def edit_404():
	flash('Please select the profile you want to edit')
	return redirect(url_for('show_profiles'))

@app.route('/edit/<profileid>',methods=["GET","POST"])
def edit_profile(profileid):
	"""docstring for edit_profile"""
	profile_info = profiles.find_one(ObjectId(profileid))
	if request.method == "POST":
		pass
	return	render_template('edit.html', profile_info=profile_info)

@app.route('/register', methods=["POST","GET"])	
def register():
	"""docstring for register"""
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		confirm = request.form["confirm"]
		if confirm == password:
			passhash = generate_password_hash(password)
			new_user = {'username':username, 'password':passhash}
			check_insert = users.insert(new_user)
			if check_insert:
				return redirect(url_for('show_profiles'))
			else:
				#not done and error occured
				flash("For some reason it didn't work, try again")
		else:
			#dont proceed
			flash("Please enter the password same twice")
	return render_template('register.html')
	
	
@app.route('/login', methods=["GET","POST"])
def login():
	"""docstring for login"""
	#loginform = loginForm(request.form)
	error = None
	if request.method == "POST":
		accuser = request.form['username']
		check_user = users.find_one({'username': accuser})
		#print check_user
		#print users.find_one()
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
	return render_template('login.html', error=error,loginpage=True)
	
@app.route('/logout')
def logout():
	"""docstring for logout"""
	session.pop('logged_in', None)
	flash('logged out')
	return redirect(url_for('show_profiles'))
	
if __name__ == "__main__":
	app.run()