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

cur.execute('''CREATE TABLE IF NOT EXISTS user_info (email text, password text, id text, image integer, token integer, CONSTRAINT email_id PRIMARY KEY (email,id))''')
cur.execute('''CREATE TABLE IF NOT EXISTS rating (id text, threestar integer, fourstar integer, fivestar integer, totalstar integer,fivestarstrak integer, solutionaday integer)''')
cur.execute('''CREATE TABLE IF NOT EXISTS request (id text, question text, image text, requester text, expertise text, date text)''')
cur.execute('''CREATE TABLE IF NOT EXISTS inboxinfo (id text, pic text, expertise text)''')
cur.execute('''CREATE TABLE IF NOT EXISTS expertise (email text, id text, expertise text)''')
cur.execute('''CREATE TABLE IF NOT EXISTS achievement (id text, achievement integer, date text, done integer)''')

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
		expertise = [x.strip() for x in expertise]
		expertise = list(set(expertise))
		try:
			cur.execute("INSERT INTO user_info VALUES (?,?,?,?,?)", (email,password,user_id,0,5))
		except sqlite3.IntegrityError:
			return render_template("signup.html", warning="Sorry, email already taken.")
		for e in expertise:
			cur.execute("INSERT INTO expertise VALUES (?,?,?)", (email,user_id,e))
		#achievement generation
		cur.execute("INSERT INTO rating VALUES (?,?,?,?,?,?,?)", (user_id, 0,0,0,0,0,0))
		for achievement in achievement_l:
			print(type(int(achievement['num'])))
			cur.execute("INSERT INTO achievement VALUES (?,?,?,?)", (user_id,int(achievement['num']),"",0))
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

def extract(user_id, rq_time = None, rating = None):
	cur.execute("SELECT expertise from expertise where id=?", (user_id,))
	expertise = cur.fetchall()
	expertise = [elt[0] for elt in expertise]
	#if not expertise:
		#print("no")
	#lst=['a'.strip(),'b'.strip()]
	_expertise=["expertise='"+x+"'" for x in expertise]
	_expertise =  " or ".join(_expertise)
	print(expertise)
	print("SELECT * from request where "+_expertise+" and not requester=?")
	cur.execute("SELECT * from request where "+_expertise+" and not requester=?", (user_id,))
	rtable = cur.fetchall()
	cur.execute("SELECT image from user_info where id = ?", (user_id,))
	img = cur.fetchone()[0]
	cur.execute("SELECT token from user_info where id=?", (user_id,))
	token = cur.fetchone()[0]
	req = []
	if rq_time :
		achievements = achievement_decision(user_id, rq_time, rating)
	else:
		achievements = []
	print("achievements")
	print(achievements)
	for i in rtable:
		print(i)
		cur.execute("SELECT image from user_info where id = ?", (i[3],))
		image = cur.fetchone()[0]
		req.append(image)

	return render_template("inbox.html", user_id=user_id, myexpertise = expertise, token=token, rtable=rtable, count = len(rtable), img = img, req = req, achievements = achievements)

@app.route('/signup')
def signup():
	return render_template("signup.html")

@app.route('/inbox',methods=['GET', 'POST'])
def inbox():
	# this will have the rating on level of understanding
	under = (request.args.get("under"))
	# this will have rate of satisfaction
	sat = (request.args.get("sat"))
	# if replied, this will have the respondent it
	replied = (request.args.get("replied"))
	user_id = request.args.get('user_id')
	if replied:
		under = int(under)
		sat = int(sat)
		adder = 1 if sat < 3 else 2
		cur.execute("UPDATE user_info SET token=token+"+str(adder)+" WHERE id=?",(user_id,))
		conn.commit()
		# TODO do sth with achievement
		# update user's achievement related info
		# cur.execute('''CREATE TABLE IF NOT EXISTS rating (id text, threestar integer, fourstar integer, fivestar integer, totalstar integer,fivestarstrak integer, solutionaday integer)''')
		cur.execute("UPDATE rating SET totalstar=totalstar+1 WHERE id=?", (user_id,))
		if sat ==1 :
			cur.execute("UPDATE rating SET fivestarstrak=0 WHERE id=?", (user_id,))
		elif sat ==2 :
			cur.execute("UPDATE rating SET fivestarstrak=0 WHERE id=?", (user_id,))

		elif sat == 3:
			cur.execute("UPDATE rating SET fivestarstrak=0 WHERE id=?", (user_id,))
			cur.execute("UPDATE rating SET threestar=threestar+1 WHERE id=?", (user_id,))
		elif sat == 4:
			cur.execute("UPDATE rating SET fivestarstrak=0 WHERE id=?", (user_id,))
			cur.execute("UPDATE rating SET fourstar=fourstar+1 WHERE id=?", (user_id,))
		elif sat == 5:
			cur.execute("UPDATE rating SET fivestarstrak=fivestarstrak+1 WHERE id=?", (user_id,))
			cur.execute("UPDATE rating SET fivestar=fivestar+1 WHERE id=?", (user_id,))
		conn.commit()
		return extract(user_id, request.args.get("request_time"), sat)

	print(user_id)
	var= request.method
	print(var)
	if request.args.get('type') == 'request' :
		print(var)
		return request_paged(request)
	elif request.args.get('type') == 'file':
		_file = request.files['image']
		if _file:
			_file.save(os.path.join("./static/propic", user_id + ".png"))
			cur.execute("UPDATE user_info SET image = 1 WHERE id = ?", (user_id,))
			conn.commit()
		else:
			warning = "Photo not specified"
			return render_template("inbox.html", warning=warning)
		return extract(user_id)

	return extract(user_id)
	#return render_template("inbox.html", user_id=user_id)
@app.route('/chat', methods=["GET"])
def chat():
	user_id=request.args.get("user_id")
	request_id = request.args.get("request")
	print(request_id)
	cur.execute("SELECT * from request where id='%s'" %request_id)
	request_obj = cur.fetchone()
	print("request object")
	print(request_obj)

	respondent = request.args.get("respondent")
	requester = False
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
		url = "http://115.68.222.144:3000/chat?user_id=%s&respondent=%s&request=%s&flag=true" %(user_id,respondent,request_id)
		msg = ("From %s\r\nTo: %s\r\nSubject:Your request is being responded\r\n\r\n %s is trying to help you. Log into chat in %s" %('donotreplyswiftyq@gmail.com',respondent_email,user_id,url))
		s.sendmail('donotreplyswiftyq@gmail.com',respondent_email,msg)
	return render_template("chat.html",user_id=user_id,respondent=respondent,requester=requester	, question = request_obj[1], img = request_obj[2], request_time = request_obj[5])

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
		#print(message)
		if "You successfully helped your requester" in message:
			to_client['type'] = 'exit'
		elif "Your requester wants a quiz" in message:
			to_client['type'] = 'quiz'
		elif "You have successfully answered" in message:
			to_client['type'] = 'answer'
		to_client['time'] = "%02d:%02d" %(datetime.datetime.now().hour%12,datetime.datetime.now().minute)
	# emit("response", {'data': message['data'], 'username': session['username']}, broadcast=True)
	print("type: " + to_client['type'])
	print (to_client)
	send(to_client, broadcast=True)

@app.route('/achievement')
def achievement():
	user_id = request.args.get("user_id")
	print("yay")
	cur.execute("SELECT * from achievement where id=?", (user_id,))
	achievements = cur.fetchall()
	cur.execute("SELECT * from achievement where id=? and done=? ORDER BY RANDOM() LIMIT 7", (user_id, 0,))
	non_achieved = cur.fetchall()
	cur.execute("SELECT count(*) from achievement where id=? and done=?", (user_id, 1,))
	achieve_num = cur.fetchall()
	#print(achievements)
	non_to_send=[]
	cur.execute("SELECT image from user_info where id = ?", (user_id,))
	img = cur.fetchone()[0]
	cur.execute("SELECT expertise from expertise where id=?", (user_id,))
	expertise = cur.fetchall()
	expertise = [elt[0] for elt in expertise]
	#if not expertise:
		#print("no")
	#lst=['a'.strip(),'b'.strip()]
	_expertise=["expertise='"+x+"'" for x in expertise]
	_expertise =  " or ".join(_expertise)
	print(expertise)
	print("SELECT * from request where "+_expertise+" and not requester=?")
	cur.execute("SELECT * from request where "+_expertise+" and not requester=?", (user_id,))
	rtable = cur.fetchall()
	print(rtable)
	for non in non_achieved:
		non_to_send.append(achievement_l[non[1]])
		#print(achievement_l[non[1]])
	return render_template("achievement.html", user_id=user_id, achievements = achievements, non_achieved = non_to_send, achieve_num = achieve_num[0][0], img = img, rtable= rtable)




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
	cur.execute("INSERT INTO request VALUES (?,?,?,?,?,?)", (_id,question,filename,user_id,expertise,date,))
	cur.execute("UPDATE user_info SET token=token-1 where id=?", (user_id,))
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
	return extract(user_id)

def update_achievements(user_id,achievements,number):
	cur.execute("SELECT * FROM achievement where id = ? and achievement = ?", (user_id, number))
	achiev = cur.fetchone()
	if achiev[3] ==0:
		achievements.append(achievement_l[number])
		cur.execute("UPDATE achievement SET done = 1 WHERE id = ? and achievement = ?", (user_id, number))
	return achievements

def achievement_decision(user_id, rq_time, single_rating):
	cur.execute("SELECT * from rating where id=?", (user_id,))
	rating = cur.fetchone()
	achievements = []
	#2017-11-25T22:13:35.868550
	rq_dt = datetime.datetime.strptime(rq_time, '%Y-%m-%dT%H:%M:%S.%f')
	cur_dt = datetime.datetime.now()
	dt_diff = (cur_dt - rq_dt).seconds/60
	##(id text, threestar integer, fourstar integer, fivestar integer, totalstar integer,fivestarstrak integer, solutionaday integer
	# 0 get first three star from user rating
	if rating[1] == 1:
		achievements = update_achievements(user_id,achievements,0)
	# 1 get first four star from user rating
	if rating[2] == 1:
		achievements = update_achievements(user_id,achievements,1)
	# 2 get first five star from user rating
	if rating[3] == 1:
		achievements = update_achievements(user_id,achievements,2)
	# 3 exchange 100 utterances with a person
	# 4 explain 10 problems
	if rating[4] == 10:
		achievements = update_achievements(user_id,achievements,4)
	# 5 explain 30 problems
	if rating[4] == 30:
		achievements = update_achievements(user_id,achievements,5)
	# 6 explain 50 problems
	if rating[4] == 50:
		achievements = update_achievements(user_id,achievements,6)
	# 7 explain 100 problems
	if rating[4] == 100 :
		achievements = update_achievements(user_id,achievements,7)
	# 8 explain 10 problems a day
	if rating[6] == 10:
		achievements = update_achievements(user_id,achievements,8)
	# 9 explain 20 problems for 20 days
	# 10 get 3 five stars consecutively
	if rating[5] == 3:
		achievements = update_achievements(user_id,achievements,10)
	# 11 get 4 stars by solving a problem in 5 minutes
	if single_rating == 4 and dt_diff<5:
		achievements = update_achievements(user_id, achievements, 11)
	# 12 get 5 stars by solving a problem in 5 minutes
	if single_rating == 5 and dt_diff<5:
		achievements = update_achievements(user_id, achievements, 12)
	# 13 get 5 five stars from user rating
	if rating[3] == 5:
		achievements = update_achievements(user_id,achievements,13)
	# 14 get 10 five stars from user rating
	if rating[3] == 10:
		achievements = update_achievements(user_id,achievements,14)
	# 15 get 20 five stars from user rating
	if rating[3] == 20:
		achievements = update_achievements(user_id,achievements,15)
	# 16 get one star from user rating
	if single_rating == 1:
		achievements = update_achievements(user_id, achievements, 16)
	# 17 post a question for 20 days
	# 18 ask 5 questions a day
	# 19 ask 10 questions a day
	conn.commit()
	return achievements

#@app.route('/achievement_list', methods=['POST'])
#def achievement_list():
#	return achievement_l

if __name__ == '__main__':
	s = smtplib.SMTP('smtp.gmail.com',587)
	s.starttls()
	s.login('donotreplyswiftyq@gmail.com', 'swiftyqadmin')
	socket_io.run(app, host='0.0.0.0', debug=True, port=3000)
