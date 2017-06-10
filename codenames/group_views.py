from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_socketio import join_room, leave_room, emit

from codenames import app, socketio
from codenames.group import Group
from codenames.gameboard import Gameboard
import json


def user_login(username, groupname):
	session['user'] = username
	session['group'] = groupname
	session['team'] = 'red'
	join_room(groupname)

@socketio.on('create group')
def create_group_view(data):
	group_name = data['groupname']
	if Group.group_exists(group_name):
		socketio.emit('alert room', 'you cannot do that')
	else:
		user_login(data['username'], data['groupname'])
		Group.start_new_game(group_name)
		socketio.emit('alert room', session['user'] + " has joined the team.", room=session['group'])
		emit('join room', Group.get_game_data(group_name))
		# data = Group.start_new_game(group_name)

@socketio.on('join group')
def join_group_view(data):
	group_name = data['groupname']
	print('trying to join ' + group_name)
	if Group.group_exists(group_name):
		print('group exists')
		user_login(data['username'], data['groupname'])
		emit('join room', Group.get_game_data(group_name), room=session['group'])
	else:
		socketio.emit('alert room', 'you cannot do that')

@socketio.on('team won round')
def team_won_round(data):
	#all users can now vote
	pass

@socketio.on('vote to start new round')
def vote_to_start_new_round(data):
	#decrement vote counters

	can_restart_now = False
	if can_restart_now:
		Group.start_new_game(session['group'])
		#prevent users from voting now
		socketio.emit('join room', room=session['group'])
	else:
		socketio.emit('alert room', room=session['group'])

