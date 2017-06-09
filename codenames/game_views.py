from codenames import app, socketio
from codenames.group import Group

@app.route('/play/')
def index():
	return render_template('index.html')


@socketio.on('click word')
def click_item(data):
	socketio.emit('notify click', {'index' : data['index'], 'team' : session['team']}, room=session['group'])
	Group.click_group_gameboard(session['group'], data['index'])


	