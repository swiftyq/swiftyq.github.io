#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask import request
from flask_socketio import SocketIO, send
from subprocess import call
from time import time
from math import log
import json
import achievement_list_opener

app = Flask(__name__)
socket_io = SocketIO(app)

achievement_l = achievement_list_opener.returner()
print(achievement_l)
print(type(achievement_l))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/inbox')
def inbox():
    return render_template("inbox.html")

@app.route('/chat')
def chat():
    return render_template("chat.html")

@app.route('/achievement')
def achievement():
    return render_template("achievement.html")

@app.route('/achievement_list', methods=['POST'])
def achievement_list():
    return achievement_l

if __name__ == '__main__':
    socket_io.run(app, host='0.0.0.0', debug=True, port=5000)
