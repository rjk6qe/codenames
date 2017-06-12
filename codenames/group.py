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

	@classmethod
	def __get_gameboard(cls, group_name):
		return json.loads(cls.__get_group(group_name).gameboard)

	@classmethod
	def get_num_users(cls, group_name):
		group = cls.__get_group(group_name)
		return group.get_user_count()

	@classmethod
	def start_new_game(cls, group_name):
		if cls.group_exists(group_name):
			group = cls.__get_group(group_name)
			group.gameboard = json.dumps(Gameboard.get_new_gameboard())
		else:
			gameboard = json.dumps(Gameboard.get_new_gameboard())
			group = models.Group(group_name, gameboard)

		db.session.add(group)
		db.session.commit()

	@classmethod
	def get_game_data(cls, group_name):
		if cls.group_exists(group_name):
			group = cls.__get_group(group_name)
			data = {}
			data['gameboard'] = group.get_gameboard()
			data['score'] = cls.get_current_score(group_name)
			data['starter'] = group.get_starter()
			data['current_turn'] = group.get_current_turn()
			return data
		else:
			return None

	@classmethod
	def set_game_data(cls, group_name, data):
		group = cls.__get_group(group_name)
		group.gameboard = data
		db.session.add(group)
		db.session.commit()

	@classmethod
	def click_group_gameboard(cls, group_name, index):
		gameboard = cls.__get_gameboard(group_name)
		new_gameboard = Gameboard.click_gameboard(gameboard, index)
		cls.set_game_data(group_name, json.dumps(new_gameboard[0]))
		return new_gameboard[1]

	@classmethod
	def join_team(cls, user_name, group_name, color):
		group = cls.__get_group(group_name)
		if color == 'red':
			group.red_count = group.red_count + 1
		if color == 'blue':
			group.blue_count = group.blue_count + 1

		db.session.add(group)
		db.session.commit()

	@classmethod
	def quit_team(cls, user_name, group_name, color):
		group = cls.__get_group(group_name)
		if color == 'red':
			group.red_count = group.red_count - 1
		if color == 'blue':
			group.blue_count = group.blue_count - 1
		db.session.add(group)
		db.session.commit()

	@classmethod
	def get_blue_count(cls, group_name):
		return cls.__get_group(group_name).get_blue_count()

	@classmethod
	def get_red_count(cls, group_name):
		return cls.__get_group(group_name).get_red_count()

	@classmethod
	def get_current_score(cls, group_name):
		group = cls.__get_group(group_name)
		return {'red': group.get_red_score(), 'blue':group.get_blue_score()}

	@classmethod
	def switch_turn(cls, group_name):
		group = cls.__get_group(group_name)
		if group.get_current_turn() == 'red':
			group.current_turn = 'blue'
		else:
			group.current_turn = 'red'
		db.session.add(group)
		db.session.commit()

		return {'current_turn' : group.current_turn}

	@classmethod
	def update_score(cls, group_name, team, color_clicked):
		print('updating score. they clicked ' + color_clicked)
		group = cls.__get_group(group_name)
		if color_clicked == 'red':
			group.red_score = group.red_score - 1
		elif color_clicked == 'blue':
			group.blue_score = group.blue_score - 1
		elif color_clicked == 'black':
			if team == 'red':
				group.blue_score = 0
			if team == 'blue':
				group.red_score = 0
		else:
			pass

		db.session.add(group)
		db.session.commit()

		return cls.get_current_score(group_name)

	@classmethod
	def team_win(cls, group_name, team):
		group = cls.__get_group(group_name)
		if team == 'red':
			group.red_wins = group.red_wins + 1
		if team == 'blue':
			group.blue_wins = group.blue_wins + 1

		db.session.add(group)
		db.session.commit()

