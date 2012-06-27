from flask import Flask
from flaskext.wtf import TextField, TextAreaField, Form, SubmitField


class TemplateSimple(Form):
	"""
	Template Simple
	"""
	Title = TextField('Profile Title')
	Unique = TextField('Unique Name')
	Intro = TextAreaField('Introduction')
	Design = TextAreaField('Design & Construction')
	Dos = TextAreaField('Dos & Donts')
	Materials = TextAreaField('Materials & Labour')
	Advantages = TextAreaField('Advantages & Limitations')
	submit = SubmitField('Submit')