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

# cur.execute('''CREATE TABLE user_info (id text primary key, password text, name text, expertise text)''')
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
	print (request.form)
	if request.form['type'] == 'signup':
		user_id = request.form['email']
		password = request.form['password1']
		name =  request.form['name']
		expertise = request.form['expertise']
		expertise = expertise.split(",")[:-1]
		print (expertise)
		for e in expertise:
			cur.execute("INSERT INTO user_info VALUES (?,?,?,?)", (user_id,password,name,e))
		conn.commit()
		return render_template("index.html")
	else:
		user_id = request.form['email']
		password = request.form['password']
		query = "SELECT  * from user_info where id='%s' and password='%s'" %(user_id,password)
		print (query)
		cur.execute(query)
		user_info = cur.fetchall()
		print (user_info)
		if not user_info:
			warning = "Incorrect id or password. Please try again."
			return render_template("index.html", warning=warning)
		return extract(user_id)

def extract(user_id):
	cur.execute("SELECT expertise from user_info where id=?", (user_id,))
	expertise = cur.fetchone()
	#if not expertise:
		#print("no")
	for x in range(0, 3):
		cur.execute("INSERT INTO request VALUES (?,?,?,?,?,?)", ("1", "hi!", "john", "john", expertise[0], "11/11",))
	cur.execute("SELECT * from request where expertise = ?", (expertise[0],))
	rtable = cur.fetchall()
	cur.execute("SELECT COUNT(id) from request where expertise = ?", (expertise[0],))
	count = cur.fetchone()[0]
	mylist = []

	return render_template("inbox.html", user_id = user_id, expertise = expertise[0], rtable=rtable, count = count)

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/inbox',methods=['GET', 'POST'])
def inbox():
	print(request.method)
	print(request.form["email"])
	return render_template("inbox.html")

@app.route('/chat', methods=["GET"])
def chat():
	user_id=request.args.get("user_id")
	return render_template("chat.html",user_id=user_id)

@socket_io.on("message", namespace='/chat')
def msg(message,username):

	print("message : "+ message)
	print("username :"+ username)
	to_client = dict()
	if message == 'new_connect':
		to_client['message'] = username+" has entered the room."
		to_client['message'] = to_client['message']
		to_client['type'] = 'connect'
		to_client['username'] = username
	else:
		to_client['message'] = message
		to_client['username'] = username
		to_client['type'] = 'normal'
		to_client['time'] = "%02d:%02d" %(datetime.datetime.now().hour%12,datetime.datetime.now().minute)
	# emit("response", {'data': message['data'], 'username': session['username']}, broadcast=True)
	send(to_client, broadcast=True)

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
