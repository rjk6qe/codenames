from codenames import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


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
	# users = relationship("User", back_populates="Groups")

	def __init__(self, name, gameboard):
		self.name = name
		self.gameboard = gameboard

	def get_gameboard(self):
		return self.gameboard

	def get_name(self):
		return self.name

# class User(db.Model):
# 	__tablename__ = "User"
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(80))
# 	team = db.Column(db.String(10))
# 	group_id = db.Column(db.String(50, ForeignKey('Groups.id')))
# 	group = relationship("Group", back_populates="User")

# 	def __init__(self, username, group):
# 		self.username = username
# 		self.group = group