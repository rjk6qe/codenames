from codenames import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import json

class Word(db.Model):
	__tablename__ = "Words"
	word = db.Column(db.String(50), primary_key=True)

	def __init__(self, word):
		self.word = word

	def get_word(self):
		return self.word

class Group(db.Model):
	__tablename__ = "Groups"
	
	id = db.Column(db.Integer, primary_key=True)
	
	name = db.Column(db.String(50), unique=True)
	gameboard = db.Column(db.Text())

	clue = db.Column(db.String(50))
	clicks_remaining = db.Column(db.Integer)
	
	starter = db.Column(db.String(5))
	current_turn = db.Column(db.String(5))
	
	red_count = db.Column(db.Integer)
	blue_count = db.Column(db.Integer)
	
	red_wins = db.Column(db.Integer)
	blue_wins = db.Column(db.Integer)

	max_wins = db.Column(db.Integer)

	red_score = db.Column(db.Integer)
	blue_score = db.Column(db.Integer)

	users = db.relationship('User', backref="group", lazy='dynamic')

	def __init__(self, name, gameboard):
		self.name = name
		self.gameboard = gameboard

		self.clue = ''
		self.clicks_remaining = 0

		self.red_count = 0
		self.blue_count = 0

		self.red_score = 9 if self.starter == 'red' else 8
		self.blue_score = 8 if self.starter == 'red' else 9

		self.red_wins = 0
		self.blue_wins = 0

		g = json.loads(self.gameboard)

		self.starter = 'red' if g['starter'] == 'R' else 'blue'
		self.current_turn = self.starter

	def get_gameboard(self):
		return json.loads(self.gameboard)

	def get_starter(self):
		return self.starter

	def get_current_turn(self):
		return self.current_turn

	def get_name(self):
		return self.name

	def get_blue_count(self):
		return self.blue_count

	def get_red_count(self):
		return self.red_count

	def get_blue_score(self):
		return self.blue_score

	def get_red_score(self):
		return self.red_score

	def get_user_count(self):
		return self.get_red_count() + self.get_blue_count()



class User(db.Model):
	__tablename__ = "Users"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	is_spymaster = db.Column(db.Boolean)
	role = db.Column(db.String(10))

	group_id = db.Column(db.Integer, db.ForeignKey('Groups.id'))

	def __init__(self, name, group_name):
		self.name = name
		self.is_spymaster = False
		self.role = 'Player'		
		self.group = Group.query.filter_by(name=group_name).first()
