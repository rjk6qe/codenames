from codenames import app, socketio

@socketio.on('login user')
def login_user_view(data):
	session['user'] = data['username']
	session['group'] = data['groupname']
	session['team'] = data['team']
	join_room(session['group'])
	socketio.emit('alert room', session['user'] + " has joined the " + session['team'] + " team.", room=session['group'])

@socketio.on('set spymaster')
def become_spymaster_view():
	#check that other users are not already spymasters
	session['is_spymaster'] = True
	socketio.emit('alert room', session['user'] + " has become the spymaster for the " + session['team'] + " team.", room=session['group'])

@socketio.on('remove spymaster')
def remove_spymaster_view():
	session['is_spymaster'] = False
	socketio.emit('alert room', session['user'] + " is no longer the spymaster for the " + session['team'] + " team.", room=session['group'])

