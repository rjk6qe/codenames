from codenames import app, socketio


@app.route('/play/')
def index():
	return render_template('index.html')