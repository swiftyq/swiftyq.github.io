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
import sqlite3
import os
import datetime
import random
import string

conn = sqlite3.connect('./static/db/userinfo.db',check_same_thread=False)
cur = conn.cursor()


#cur.execute('''CREATE TABLE info
#				(id text, password text, name text, expertise text)''')
#cur.execute('''CREATE TABLE rating
#				(id text, rating number, date text)''')
#cur.execute('''CREATE TABLE achievement
#				(id text, achievement number, date text)''')
#cur.execute('''CREATE TABLE session''')
#cur.execute('''CREATE TABLE request
#				(id number, question text, image text, requester text, expertise text, date text)''')


app = Flask(__name__)
socket_io = SocketIO(app)

# Data structure
# User-info: id, password, expertise
# rating history,
# achievement: id (text), achievement (number), date (text)
# session history
achievement_l = achievement_list_opener.returner()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/',methods=["POST"])
def login():
	if request.method == "POST":
		user_id = request.form['id']
		password = request.form['password']
		cur.execute("SELECT  * from info where id=? and password=?", (user_id,password,))
		user_info = cur.fetchone()
		if not user_info:
			warning = "Incorrect id or password. Please try again."
			return render_template("index.html", warning=warning)
	return render_template("inbox.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signedup', methods=["POST"])
def signedup():
	print(request.form)
	user_id = request.form['id']
	password = request.form['password']
	name =  request.form['name']
	expertise = request.form['expertise']
	expertise = expertise.split(",")[:-1]
	for e in expertise:
		cur.execute("INSERT INTO info VALUES (?,?,?,?)", (user_id,password,name,e))
	conn.commit()
	return render_template("index.html")

@app.route('/inbox',methods=['GET', 'POST'])
def inbox():
	print(request.method)
	print(request.form["email"])
	return render_template("inbox.html")

@app.route('/chat')
def chat():
    return render_template("chat.html")

@app.route('/achievement')
def achievement():
    return render_template("achievement.html")

@app.route('/request_page')
def request_page():
    print("rrrequest!")
    return render_template("request.html")

@app.route('/request_paged',methods=['POST'])
def request_paged():
    question = request.form['question']
    expertise = request.form['expertise']
    _file = request.files['image']
    if not question:
        warning = "Question not specified. Please ask a question."
        return render_template("request.html", warning=warning)
    if not expertise:
        warning = "Expertise not specified. Please specify expertise."
        return render_template("request.html", warning=warning)
    print(_file)
    date = datetime.datetime.now().isoformat()
    print(date)

    _id = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
    #cur_date =
    if _file:
        _file.save(os.path.join("./static/upload", _id + ".png"))
        filename = _id+".png"
    else:
        filename=""
    cur.execute("INSERT INTO request VALUES (?,?,?,?,?,?)", (_id,question,filename,"requester",expertise,date))
    conn.commit()
    return render_template("inbox.html")


@app.route('/achievement_list', methods=['POST'])
def achievement_list():
    return achievement_l

if __name__ == '__main__':
    socket_io.run(app, host='0.0.0.0', debug=True, port=5000)
