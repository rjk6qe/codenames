from flask import render_template, session

from codenames import app, socketio
from codenames.group import Group

@app.route('/play/')
def index():
	return render_template('index.html')

@socketio.on('click word')
def click_item(data):
	print("index " + data['index'])
	color = Group.click_group_gameboard(session['group'], int(data['index']))
	socketio.emit('alert click', {'index' : data['index'], 'team' : session['team'], 'color' : color, 'onLoad':False}, room=session['group'])