from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_socketio import SocketIO, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://onqueetfxnebhf:334c1af97933892d50d159dbe859f6c2e41c96c116a68d05d90c3d47c1a93cb9@ec2-54-243-252-91.compute-1.amazonaws.com:5432/d58d83185633ra"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = "\x11\xe2\xc1\xe9\x89\x9eZp\xef\xf3q\xb0\xcd\xe3\x15\xbd#f\xd8\x91\x87E'\xf0"

from codenames.group import Group

def user_login(username, groupname, role, team):
	session['logged_in'] = True
	session['role'] = role
	session['user'] = username
	session['group'] = groupname
	session['team'] = team
	join_room(groupname)
	Group.join_team(
		session['user'],
		session['group'],
		session['team']
		)

def user_logout():
	leave_room(session['group'])
	Group.quit_team(
		session['user'],
		session['group'],
		session['team']
		)

def user_group_data(group_name):
	return_data = Group.get_game_data(group_name)
	return_data['team'] = session['team']
	return_data['role'] = session['role']
	print(return_data)
	print(type(return_data))
	print('\n')
	print(json.dumps(return_data))
	return json.dumps(return_data)

@socketio.on('connect')
def connect():
	print("CONNECTING")
	if not session.get('logged_in', False):
		session['user'] = ''
		session['group'] = ''
		session['role'] = ''
		session['team'] = ''
		session['logged_in'] = False
	else:
		print(session['user'] + " connected")
		join_group_view({'groupname': session['group'], 'username':session['user']})

@socketio.on('disconnect')
def disconnect():
	print("DISCONNECTING")
	if session['logged_in']:
		print(session['user'] + " disconnected")
		user_logout()
		if session['role'] == 'Host':
			socketio.emit('alert room', 'Host disconnected, rejoining room...', room=session['group'])
			socketio.emit('join room', user_group_data(session['group']), room=session['group'])
		else:
			socketio.emit('alert room', session['user'] + ' has left the group', room=session['group'])

import codenames.group_views
import codenames.user_views
import codenames.game_views