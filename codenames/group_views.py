from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_socketio import join_room, leave_room, emit

from codenames import app, socketio, user_login, user_logout, user_group_data
from codenames.group import Group
from codenames.gameboard import Gameboard

from codenames.game_views import spymaster_submit_clue

import json
import random

def assign_team(group_name):
	print('assigning user to team ' + group_name)
	if session.get('team', '') == '':
		print('user does not already have a team')
		print('curr_team: ' + session.get('team', ''))
		num_red = Group.get_red_count(group_name)
		num_blue = Group.get_blue_count(group_name)
		print('there are ' + str(num_red) + ' red users, and ' + str(num_blue) + ' blue users')

		if num_red > num_blue:
			print('assigning to team blue')
			return 'blue'
		elif num_blue > num_red:
			print('assigning to team red')
			return 'red'
		else:
			print('randomly assigning')
			return 'red' if random.randint(0,1) else 'blue'
	else:
		print('already in team ' + session['team'])
		return session['team']

def assign_role(group_name):
	if session.get('role', '') == '':
		print('user did not already have a role')
		num_users = Group.get_num_users(group_name)
		print('there are ' + str(num_users) + ' users in group ' + group_name)
		return 'Host' if num_users == 0 else 'Player'
	else:
		print('already had role ' + session['role'])
		return session['role']

@socketio.on('create group')
def create_group_view(data):
	group_name = data['groupname']
	user_name = data['username']

	if Group.group_exists(group_name):
		emit('alert room', 'Cannot create group because it already exists')
	else:
		Group.start_new_game(group_name)
		role = assign_role(group_name)
		team = assign_team(group_name)
		user_login(
			data['username'],
			data['groupname'],
			role,
			team
			)
		emit('join room', user_group_data(session['group']))
		spymaster_submit_clue({'clue':'pick a word', 'guesses': 3})


@socketio.on('join group')
def join_group_view(data):
	group_name = data['groupname']
	user_name = data['username']
	if Group.group_exists(group_name):
		role = assign_role(group_name)
		team = assign_team(group_name)
		user_login(
			user_name,
			group_name,
			role,
			team
			)
		emit('join room', user_group_data(session['group']))
		socketio.emit('alert room', session['user'] + " has joined the game.", room=session['group'])
		spymaster_submit_clue({'clue':'pick a word', 'guesses': 3})
	else:
		emit('alert room', 'You cannot join the group because it does not exist')

