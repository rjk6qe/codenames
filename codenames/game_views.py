from flask import render_template, session

from codenames import app, socketio, user_group_data
from codenames.group import Group

import json

@app.route('/play/')
def index():
	return render_template('index.html')

@socketio.on('spymaster submit')
def spymaster_submit_clue(data):
	print('spymaster submitted a clue')
	clue = data['clue']
	available_guesses = data['guesses']

	data = {'clue':clue, 'guesses' : available_guesses}
	socketio.emit('clue submitted', json.dumps(data), room=session['group'])

@socketio.on('click word')
def click_item(data):
	color = Group.click_group_gameboard(session['group'], int(data['index']))
	score = Group.update_score(session['group'], session['team'], color)

	if score['red'] == 0 or score['blue'] == 0:
		return_data = {'winner': 'red' if score['red'] == 0 else 'blue'}
		socketio.emit('round over', json.dumps(return_data), room=session['group'])

	if color != session['team']:
		if color == 'black':
			socketio.emit('alert click assassin', room=session['group'])
		else:
			#tell spymaster to enter a new clue
			spymaster_submit_clue({'clue':'oh hey there', 'guesses':5})	

			socketio.emit('switch turn', json.dumps(Group.switch_turn(session['group'])), room=session['group'])

	#score, index, color
	return_dict = {'score': score, 'index':data['index'], 'color':color}
	socketio.emit('alert click', json.dumps(return_dict), room=session['group'])

@socketio.on('end turn')
def end_turn(data):
	socketio.emit('switch turn', json.dumps(Group.switch_turn(session['group'])), room=session['group'])

@socketio.on('start new round')
def start_new_game(data):
	Group.start_new_game(session['group'])
	socketio.emit('join room', user_group_data(session['group']), room=session['group'])
