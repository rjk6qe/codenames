from codenames import db
from codenames.gameboard import Gameboard
import codenames.models as models
import json

class User:
	
	table = models.User

	@classmethod
	def __get_user(cls, user_name):
		return cls.table.query.filter_by(name=user_name).first()

	@classmethod
	def __user_exists(cls,user_name):
		return cls.table.query.filter_by(name=user_name).count() != 0

	@classmethod
	def assign_team(cls, user_name, team):
		user = cls.__get_user(user_name)
		user.team = team
		db.session.add(user)
		db.session.commit()

	@classmethod
	def assign_role(cls, user_name, role):
		user = cls.__get_user(user_name)
		user.role = role
		db.session.add(user)
		db.session.commit()


