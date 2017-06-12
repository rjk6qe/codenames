import unittest
from codenames.group import Group
from codenames.gameboard import Gameboard

import codenames.models as models

import random

class TestGameboard(unittest.TestCase):

	group_table = models.Group
	random_name = str(random.random())


	def test_create_group(self):


		Group.start_new_game(random_name)


		self.assertEqual(

			)


