from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_socketio import SocketIO, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy

import json
import random

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://onqueetfxnebhf:334c1af97933892d50d159dbe859f6c2e41c96c116a68d05d90c3d47c1a93cb9@ec2-54-243-252-91.compute-1.amazonaws.com:5432/d58d83185633ra"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = "\x11\xe2\xc1\xe9\x89\x9eZp\xef\xf3q\xb0\xcd\xe3\x15\xbd#f\xd8\x91\x87E'\xf0"

import codenames.group_views
import codenames.user_views
import codenames.game_views