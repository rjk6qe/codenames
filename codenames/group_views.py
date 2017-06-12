from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_socketio import join_room, leave_room, emit

from codenames import app, socketio, user_login, user_logout, user_group_data
from codenames.group import Group
from codenames.gameboard import Gameboard

import json
import random

def assign_team(group_name):
	num_red = Group.get_red_count(group_name)
	num_blue = Group.get_blue_count(group_name)

	if num_red > num_blue:
		return 'blue'
	elif num_blue > num_red:
		return 'red'
	else:
		return 'red' if random.randint(0,1) else 'blue'

def assign_role(group_name):
	num_users = Group.get_num_users(group_name)
	return 'Host' if num_users == 0 else 'Player'

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
	else:
		emit('alert room', 'You cannot join the group because it does not exist')

