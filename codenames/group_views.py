from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_socketio import join_room, leave_room, emit

from codenames import app, socketio
from codenames.group import Group
from codenames.gameboard import Gameboard
import json


def set_user_role(role):
	session['role'] = role

def user_login(username, groupname, role):
	set_user_role(role)
	session['user'] = username
	session['group'] = groupname
	session['team'] = 'red'
	join_room(groupname)
	Group.add_user(session['group'])

def user_logout(groupname):
	print('logging user out')
	leave_room(groupname)
	Group.remove_user(groupname)
	session.pop('user')
	session.pop('group')
	session.pop('team')
	session.pop('role')

@socketio.on('create group')
def create_group_view(data):
	group_name = data['groupname']
	if Group.group_exists(group_name):
		socketio.emit('alert room', 'you cannot do that')
	else:
		Group.start_new_game(group_name)
		user_login(data['username'], data['groupname'], data['role'])
		socketio.emit('alert room', session['user'] + " has joined the team.", room=session['group'])
		emit('join room', Group.get_game_data(group_name))
		# data = Group.start_new_game(group_name)

@socketio.on('join group')
def join_group_view(data):
	group_name = data['groupname']
	print('trying to join ' + group_name)
	if Group.group_exists(group_name):
		print('group exists')
		user_login(data['username'], data['groupname'], data['role'])
		emit('join room', Group.get_game_data(group_name))
	else:
		socketio.emit('alert room', 'you cannot do that')

@socketio.on('role select')
def change_role_view(data):
	set_user_role(data['role'])

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

@socketio.on('disconnect')
def disconnect():
	if 'group' in session:
		user = session['user']
		group = session['group']
		role = session.get('role', 'no role')
		user_logout(session['group'])
		if role == 'Host':
			data = json.loads(Group.get_game_data(group))
			if int(data['num_players']) > 0:
				socketio.emit('alert room', 'Host disconnected, rejoining room...', room=group)
				socketio.emit('join room', json.dumps(data), room=group)
		else:
			socketio.emit('alert room', user + ' has left the group', room=group)
