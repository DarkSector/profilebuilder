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
from bson.objectid import ObjectId, InvalidId
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

conn = Connection(pymongoconfig.MONGO_HOST, pymongoconfig.MONGO_PORT)
dbobj = conn[pymongoconfig.MONGO_DATABASE]
users = dbobj['accesslist']
profiles = dbobj['profiles']		

@flask_sijax.route(app,'/')
def show_profiles():
	def delete_profile(obj_response,object_id):
		"""
		The delete_profile function is called along with passing a 
		correct ObjectId as object_id. 
		
		The corrosponding table row is removed simultaneously
		"""
		profiles.remove(ObjectId(object_id))
		div_id =  '"#' + object_id + '"'
		return obj_response.script('$('+div_id+').remove();')
	
	if g.sijax.is_sijax_request:
		g.sijax.register_callback('delete_this',delete_profile)
		return g.sijax.process_request()
		
	allprofiles = profiles.find()
	return render_template('index.html', profiles=allprofiles)
	
	
@app.route('/addprofile',methods=["GET","POST"])
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

@flask_sijax.route(app,'/addtags')
def addtags():
	def addnewtags(obj_response, tag):
		pass
	def deletetags(obj_response, tag):
		pass
	if g.sijax.is_sijax_request:
		g.sijax.register_callback('delete_tag', deletetags)
		g.sijax.register_callback('add_new', addnewtags)
		return g.sijax.process_request()
	
	return render_template('panel.html')
	
@app.route('/edit')
def edit_404():
	flash('Please select the profile you want to edit')
	return redirect(url_for('show_profiles'))

@flask_sijax.route(app,'/edit/<profileid>')
def edit_profile(profileid):
	"""
	The profile has to be edited. The following page allows following 
	functions to be executed:
	
	1. Edit existing data
	2. Add new fields and data
	3. Create media gallery
	4. Edit proper paragraphs with media in them.
	5. delete fields
	"""
	try:
		"""
		The profileid may not be a valid ObjectId, if it's not a valid
		ObjectId, user must get routed to main page. 
		"""
		profile_info = profiles.find_one(ObjectId(profileid))
	except InvalidId:
		"""
		Flash message and route to main page
		"""
		flash("No such profile exists, are you sure you have the right link")
		return redirect(url_for('show_profiles'))
	else:
		profile_info = profile_info
		"""
		Gets the profile information and puts it into profile_info dict
		"""
		
	def add_data(obj_response, data):
		pass	
	def edit_data(obj_response, data):
		pass
	
		
	return	render_template('edit.html', profile_info=profile_info)


@app.route('/register', methods=["POST","GET"])	
def register():
	"""
	An admin user already logged is allowed to register new usernames
	the new usernames cannot be changed at the moment nor can they be
	deleted unless done from command line
	"""
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
	"""User logging in function"""
	error = None
	if request.method == "POST":
		accuser = request.form['username']
		check_user = users.find_one({'username': accuser})
		if check_user:
			accpass = request.form['password']
			check_pass = check_password_hash(check_user['password'],accpass)
			if check_pass:
				session['logged_in'] = True
				return redirect(url_for('show_profiles'))
			else:
				flash("Incorrect username or password")				
		else:
			flash("Incorrect username or password")
	return render_template('login.html', error=error,loginpage=True)
	
@app.route('/logout')
def logout():
	"""docstring for logout"""
	session.pop('logged_in', None)
	flash('logged out')
	return redirect(url_for('show_profiles'))

#Run application on 0.0.0.0:5000	
if __name__ == "__main__":
	app.run('0.0.0.0')