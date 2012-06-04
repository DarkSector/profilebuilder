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
from profilebuilder import conn, dbobj, users, profiles, types
from profilebuilder import app


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
		return obj_response.script('$('+div_id+').remove();'), obj_response.script("$('#profiledelete').show()")
	
	if g.sijax.is_sijax_request:
		g.sijax.register_callback('delete_this',delete_profile)
		return g.sijax.process_request()
		
	allprofiles = profiles.find()
	return render_template('index.html', profiles=allprofiles)
	
@flask_sijax.route(app,'/addprofile')
def add_profile():
	"""
	These functions handle profile adding
	"""
	def newprofile_handler(obj_response,name,unique,_type):
		"""
		name: is the profile title
		unique: is the unique title that will go into the url
		_type: is the type of the profile
		"""
		#for debug
		#print name, unique, _type
		
		#create a profile dict
		profile = {'title':name, 'unique': unique, 'profiletype' : _type }
		
		#add the profile into the profiles
		checkifAdded = profiles.insert(profile)
		
		#check if the profile is added
		if checkifAdded:
			return obj_response.script("$('#profileaddsuccess').show()")
		#if the profile is not added
		else:
			return obj_response.script("$('#profileaddfail').show()")
	
	def newtype_handler(obj_response,profilevalue):
		"""
		
		"""
		#debug
		#print profilevalue
		
		#insert type of profile
		types.insert({'name':profilevalue})
		
		#return obj_response.script('Added a new profile type :' + profilevalue), obj_response.script('$("#profileselect").append("<option value=' + profilevalue + '>' + profilevalue + '</option>")')
		return obj_response.script("$('#addType').modal('toggle')"),obj_response.script("$('#profiletypeaddsuccess').show()"),obj_response.script('$("#profileselect").append("<option value=' + profilevalue + '>' + profilevalue + '</option>")')
		
			
	if g.sijax.is_sijax_request:
			g.sijax.register_callback('save_profiletype',newtype_handler)
			g.sijax.register_callback('save_newprofile', newprofile_handler)	
			return g.sijax.process_request()
			
	typeofprofiles = types.find()
	return render_template('add.html', profiletypes=typeofprofiles)
	
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

	def editdata_handler(obj_response, data_key, data_value):
		if data_key == "" or data_value == "":
			return obj_response.alert("Value ready to put in, please close this dialog box and insert again")
		else:
			current_profile = profiles.find_one(ObjectId(profileid))
			current_profile[data_key] = data_value
			profiles.save(current_profile)
			return obj_response.alert("value stored")
		#foo = str(current_profile)
		#return obj_response.alert(foo)
	
	if g.sijax.is_sijax_request:
			g.sijax.register_callback('save_editdata',editdata_handler)
			return g.sijax.process_request()
		
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


@app.route('/view/profile/<_id>')
def render_techprofile(_id):
	#try:
	#	profileinfo = profiles.find(ObjectId(_id))
	#except InvalidId:
	#	flash("No such profile found")
	
	profileinfo = profiles.find_one(ObjectId(_id))
	return render_template('finalview.html', profileinfo=profileinfo)


#@app.route('/view/profile/<uniquename>')
#def render_techprofile(uniquename):
#	pass

#@app.route('/view/professional/<proname>')
#def render_profprofile(proname):
#	pass

#@app.route('/view/org/<orgname>')
#def render_orgprofile(orgname):
#	pass
