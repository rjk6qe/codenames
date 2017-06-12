from codenames import db
from codenames.gameboard import Gameboard
import codenames.models as models
import json

class DbInterface:

	self.model = models.User

	@staticmethod
	def exists(name):
		return self.model.query.filter_by(name=name).count() != 0

	@staticmethod
	def get_object(name):
		return self.model.query.filter_by(name=name).first()