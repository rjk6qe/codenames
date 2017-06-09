from codenames import db
from codenames.gameboard import Gameboard
import codenames.models as models
import json

class Group:


	@staticmethod
	def __get_group(group_name):
		return models.Group.query.filter_by(name=group_name).first()

	@staticmethod
	def group_exists(group_name):
		return models.Group.query.filter_by(name=group_name).count() != 0

	@staticmethod
	def get_gameboard(cls, group_name):
		return json.loads(cls.__get_group(group_name).gameboard)

	@classmethod
	def start_new_game(cls, group_name):
		if cls.group_exists(group_name):
			group = models.Group.query.filter_by(name=group_name).first()
		else:
			group = 
		group.gameboard = Gameboard.get_new_gameboard()
		db.session.add(group)
		db.session.commit()

	@classmethod
	def get_game_data(cls, group_name):
		if cls.group_exists(group_name):
			data = {}
			data['gameboard'] = cls.get_gameboard(group_name)
			spymaster_dict = {}
			spymaster_dict['red_spymaster'] = None
			spymaster_dict['blue_spymaster'] = None
			data['spymaster'] = spymaster_dict
			return json.loads(data)
		else:
			return None