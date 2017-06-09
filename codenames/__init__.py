from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_socketio import SocketIO, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy

import json
import random

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://dkurzncavtalhd:e1ed5e114531e4d412508c3612daf3cf9ef1a696764e8ca041080ca8061b8ec9@ec2-184-73-236-170.compute-1.amazonaws.com:5432/d1hgf1om6912pm"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = "\x11\xe2\xc1\xe9\x89\x9eZp\xef\xf3q\xb0\xcd\xe3\x15\xbd#f\xd8\x91\x87E'\xf0"

import codenames.group_views
import codenames.user_views
import codenames.game_views