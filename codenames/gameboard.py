from sqlalchemy.sql.expression import func

import codenames.models as models
import random

class Gameboard:

	word_model = models.Word

	@staticmethod
	def __abbr_to_color(color):
		if color == 'R':
			return 'red'
		if color == 'B':
			return 'blue'
		if color == 'C':
			return 'green'
		if color == 'A':
			return 'black'
		print('none of the above')
		print(color)
		return None

	@staticmethod
	def __create_key(is_red):
		red = 9 if is_red else 8
		blue = 8 if is_red else 9
		gameboard = (['R'] * red) + (['B'] * blue) + ['A'] + (['C'] * 7)
		random.shuffle(gameboard)
		return gameboard

	@classmethod
	def __get_wordlist(cls, develop_mode):
		words = cls.word_model.query.order_by(func.random()).limit(25).all()
		list_of_words = []
		for word in words:
			list_of_words.append(word.word.split('.')[random.randint(0,1)])
		return list_of_words

	@classmethod
	def get_new_gameboard(cls):
		gameboard = {}
		gameboard['is_red'] = bool(random.randint(0,1))
		gameboard['key'] = cls.__create_key(gameboard['is_red'])
		gameboard['word_list'] = cls.__get_wordlist(False)
		gameboard['click_map'] = [False] * 25
		gameboard['starter'] = 'R' if gameboard['is_red'] else 'B'
		return gameboard

	@classmethod
	def click_gameboard(cls, gameboard, index):
		click_map = gameboard['click_map'];
		click_map[index] = True
		key = gameboard['key']
		color = key[index]
		return {'gameboard' : gameboard, 'color':cls.__abbr_to_color(color)}