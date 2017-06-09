from codenames import db

class Word(db.Model):
	__tablename__ = "Words"
	word = db.Column(db.String(50), primary_key=True)

	def __init__(self, word):
		self.word = word

	def get_word(self):
		return self.word


class Group(db.Model):
	__tablename__ = "Groups"
	name = db.Column(db.String(50), primary_key=True)
	gameboard = db.Column(db.Text())

	def __init__(self, name, gameboard):
		self.name = name
		self.gameboard = gameboard

	def get_gameboard(self):
		return self.gameboard

	def get_name(self):
		return self.name

class User(db.Model):
	__tablename__ = "User"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	team = db.Column(db.String(10))
	is_spymaster = db.Column(db.Boolean)
	group = db.relationship('Group')

	def __init__(self, username, group):
		self.username = username
		self.group = group