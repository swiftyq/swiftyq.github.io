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
import smtplib
from email.mime.text import MIMEText

conn = sqlite3.connect('./static/db/userinfo.db',check_same_thread=False)
cur = conn.cursor()


#cur.execute('''CREATE TABLE user_info (email text, password text, id text, image integer, CONSTRAINT email_id PRIMARY KEY (email,id))''')
#cur.execute('''CREATE TABLE info
#				(id text, password text, name text, expertise text)''')
#cur.execute('''CREATE TABLE rating
#				(id text, rating number, date text)''')
#cur.execute('''CREATE TABLE achievement
#				(id text, achievement number, date text)''')
#cur.execute('''CREATE TABLE session''')
#cur.execute('''CREATE TABLE request
				#(id number, question text, image text, requester text, expertise text, date text)''')

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
		email = request.form['email']
		password = request.form['password1']
		user_id =  request.form['name']
		expertise = request.form['expertise']
		expertise = expertise.split(",")[:-1]
		print (request.form)
		cur.execute("INSERT INTO user_info VALUES (?,?,?,?)", (email,password,user_id,0))
		for e in expertise:
			cur.execute("INSERT INTO expertise VALUES (?,?,?)", (email,user_id,e))
		conn.commit()
		return render_template("index.html")
	else:
		user_id = request.form['email']
		password = request.form['password']
		query = "SELECT * from user_info where email='%s' and password='%s'" %(user_id,password)
		print (query)
		cur.execute(query)
		user_info = cur.fetchall()
		print (user_info)
		if not user_info:
			warning = "Incorrect id or password. Please try again."
			return render_template("index.html", warning=warning)
		return extract(user_info[0][2])

def extract(user_id):
	cur.execute("SELECT expertise from expertise where id=?", (user_id,))
	expertise = cur.fetchone()
	#if not expertise:
		#print("no")
	cur.execute("SELECT * from request where expertise = ? and not requester=?", (expertise[0],user_id,))
	rtable = cur.fetchall()
	cur.execute("SELECT COUNT(id) from request where expertise = ?", (expertise[0],))
	count = cur.fetchone()[0]
	mylist = []
	cur.execute("SELECT image from user_info where id = ?", (user_id,))

	req = []
	count = 0;
	for i in rtable:
		cur.execute("SELECT image from user_info where id = ?", (i[0]))
		image = fetchone()[0]
		req[count] = image
		count = count+1

	img = cur.fetchone()[0]
	return render_template("inbox.html", user_id=user_id, expertise = expertise[0], rtable=rtable, count = len(rtable), img = img, req = req)

@app.route('/signup')
def signup():
	return render_template("signup.html")

@app.route('/inbox',methods=['GET', 'POST'])
def inbox():
	user_id = request.args.get('user_id')
	var= request.method
	print(var)
	if request.args.get('type') == 'request' :
		print(var)
		return request_paged(request)
	elif request.args.get('type') == 'file':
		_file = request.files['image']
		if _file:
			_file.save(os.path.join("./static/propic", user_id + ".png"))
			cur.execute("INSERT INTO user_info (image) VALUES (?) where id =?", (1, user_id,))
		else:
			warning = "Question not specified. Please ask a question."
			return render_template("inbox.html", warning=warning)
		return extract(user_id)

	return render_template("inbox.html", user_id=user_id)
@app.route('/chat', methods=["GET"])
def chat():
	user_id=request.args.get("user_id")
	respondent = request.args.get("respondent")
	requester = ""
	flag = request.args.get("flag")
	print (flag)
	if request.args.get("flag"):
		#request handler
		requester = True
		print (requester)
	else:
		#respondent handler
		cur.execute("SELECT email from user_info where id='%s'" %respondent)
		respondent_email = cur.fetchone()[0]
		url = "http://swiftyq.herokuapp.com/chat?user_id=%s&respondent=%s&flag=true" %(user_id,respondent)
		msg = ("From %s\r\nTo: %s\r\nSubject:Your request is being responded\r\n\r\n %s is trying to help you. Log into chat in %s" %('donotreplyswiftyq@gmail.com',respondent_email,user_id,url))
		s.sendmail('donotreplyswiftyq@gmail.com',respondent_email,msg)
	return render_template("chat.html",user_id=user_id,respondent=respondent,requester=requester)

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
	#print(user_id)
	user_id = request.args.get("user_id")
	print(user_id)
	return render_template("request.html", user_id=user_id)


def request_paged(request):
	#user_id = request.form['user_id']
	global s
	user_id = request.args.get("user_id")
	print("guaack")
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
	cur.execute("INSERT INTO request VALUES (?,?,?,?,?,?)", (_id,question,filename,user_id,expertise,date))
	conn.commit()
	cur.execute("SELECT email,id FROM expertise where expertise=?", (expertise,))
	emails = cur.fetchall()
	print (emails)

	for i in emails:
		if not "@" in i[0]:
			continue
		print (i[0])
		msg = ("From %s\r\nTo: %s\r\nSubject:SwiftyQ Request\r\n\r\n Someone needs your help for %s" %('donotreplyswiftyq@gmail.com',i[0],expertise))
		s.sendmail('donotreplyswiftyq@gmail.com',i[0],msg)
	s.quit()
	return extract(user_id)


@app.route('/achievement_list', methods=['POST'])
def achievement_list():
	return achievement_l

if __name__ == '__main__':
	s = smtplib.SMTP('smtp.gmail.com',587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login('donotreplyswiftyq@gmail.com', 'swiftyqadmin')
	s.ehlo()
	socket_io.run(app, host='0.0.0.0', debug=True, port=5000)
