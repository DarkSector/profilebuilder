#!/usr/bin/python
"""
	Rural Housing Knowledge Networks - Database builder	
	Author: Pronoy Chopra
	IIT Delhi
	
"""

from __future__ import with_statement

import os
import Image
import shutil
import StringIO
import zipfile
import pymongo
from pymongo import Connection
from bson.objectid import ObjectId, InvalidId
import pymongoconfig
from flask import Flask, request, session, redirect, url_for, abort, \
     render_template, flash, g
from flask.ext.bcrypt import bcrypt, generate_password_hash, check_password_hash
import flask_sijax
from flaskext.uploads import UploadSet, configure_uploads, IMAGES, \
                              UploadNotAllowed
from werkzeug import secure_filename


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

path = os.path.join('.',os.path.dirname(__file__), '../')

app.config['SIJAX_STATIC_PATH'] = os.path.join('.',os.path.dirname(__file__), 'static/js/sijax')

app.config['UPLOADED_FILES_DEST'] = os.path.join('.', os.path.dirname(__file__),'static/img/uploadedmedia')


if not os.path.exists(app.config['UPLOADED_FILES_DEST']):
	os.makedirs(app.config['UPLOADED_FILES_DEST'])
else:
	pass


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#initialize flask_sijax
flask_sijax.Sijax(app)

#pymongo connections
conn = Connection(pymongoconfig.MONGO_HOST, pymongoconfig.MONGO_PORT)
dbobj = conn[pymongoconfig.MONGO_DATABASE]
users = dbobj['accesslist']
profiles = dbobj['profiles']
types = dbobj['profiletypes']
pros = dbobj['professionals']



#third level imports
import profilebuilder.views