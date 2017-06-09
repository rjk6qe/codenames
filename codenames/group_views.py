from codenames import app, socketio
from codenames.group import Group
from codenames.gameboard import Gameboard
import json

@app.route('/group/create', methods=['POST',])
def create_group_view():
	data = request.form
	group_name = data['name']
	if Group.group_exists(group_name):
		return json.dumps({'status':False})
	else:
		Group.start_new_game(group_name)
		return json.loads(Group.get_game_data(group_name))

@app.route('/group/join', methods=['POST',])
def join_group_view():
	data = request.form
	group_name = data['name']
	if not Group.group_exists(group_name):
		return json.dumps({'status':False})
	else:
		return json.loads(Group.get_game_data(group_name))

@socketio.on('team won round')
def team_won_round():
	#all users can now vote
	pass

@socketio.on('vote to start new round')
def vote_to_start_new_round(data):
	#decrement vote counters

	can_restart_now = False
	if can_restart_now:
		Group.start_new_game(session['group'])
		#prevent users from voting now
		socketio.emit('rejoin game', room=session['group'])
	else:
		socketio.emit('alert room', room=session['group'])

