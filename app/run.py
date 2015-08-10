#imports
from flask import Flask, send_from_directory, jsonify, render_template, request, flash, g, url_for, session, redirect, abort, views
from contextlib import closing
import datetime
import sqlite3 as lite
import sys
import json
import random
#import flask.views
#app name
app = Flask(__name__, static_url_path='/')

app.config.update( dict (
	DATABASE ='forms.db',
	DEBUG = True,
	SECRET_KEY= 'dev_key'
	))
# Declaration of important variables
nameOfTest = "Test1"
ans = []
questions = {}
#all experimental
'''The tests
	class Login(views.MethodView):
		def get(self):
			render_template('login.html')
			#also test
		def post(self):
			required = ['username','password']
			for r in required:
				if r not in request.form:
					flash("Error:{0} is required".format(r))
					return redirect(url_for('login'))
			username = request.form['username']
			password = request.form['password']
			if username in users and users[username] == password:
				session['username'] = username 
			else:
				flash("username is probably wrong")
			return redirect(url_for('login'))
	#testing
	class Survey(views.MethodView):
		def get(self):
			return render_template('index.html')

		def post(self):
			result = eval(request.form['expression'])
			flash(result)
			return self.get()
			
			
	class View(views.MethodView):
		def get(self):
			return render_template('login.html')
	#test
		def post(self):
			result = eval(request.form['expression'])
			flash(result)
			return self.get()
'''
#added for login
#app.add_url_rule('/', view_func=Login.as_view('/login'), methods=['GET','POST'])
#app.add_url_rule('/Survey/', view_func=Survey.as_view('survey'), methods=['GET', 'POST'])

'''Example taken from http://codepen.io/asommer70/blog/serving-a-static-directory-with-flask'''
#login_manager = LoginManager()
def usernameGenereator(): #returns a randomly generated username for testing purposes
	theuser = ''
	for i in range(15):
		theuser = theuser + str(random.randrange(0,10))
	return theuser

def passwordGenereator(): #returns a randomly generated password for testing purposes
	thepassword = ''
	for i in range(15):
		thepassword = thepassword + str(random.randrange(0,10))
	return thepassword

def storeUsers(username, password): #stores username and password to Users table, returns last ID
		con = lite.connect('database.db')
		returning = ''
		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO Users(AmazonID, Password) VALUES(?,?)", (username, password))
			cur.execute('SELECT max(UserID) FROM Users')
			returning = cur.fetchone()
			returning = returning[0]
		return returning

def storeSession(theid, start, stop):#stores userID, start time and end time to Sessions table, returns last ID
	con = lite.connect('database.db')
	returning = ''
	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO Sessions(UserID, Timebegan, Timeended) VALUES(?,?,?)", (theid, start, stop))
		cur.execute('SELECT max(SessionID) FROM Sessions')
		returning = cur.fetchone()
		returning = returning[0]
	return returning

def storeAnswer(theuserid, thesessionid, thequestion, theanswer): #stores userID, sessionID, question and answer to Answers table
	con = lite.connect('database.db')
	returning = ''
	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO Answers(UserID, SessionID, Question, Answer) VALUES(?,?,?,?)", (theuserid, thesessionid, thequestion, theanswer))

def loadQandA(): #loads questions from Questions table and returns them as an array(loadQuestions)
	con = lite.connect('database.db')
	returning = {}
	with con:
		cur = con.cursor()
		cur.execute('SELECT Question, Answers FROM Questions')
		rows = cur.fetchall()
		for row in rows:
			returning[row[0]] = json.loads(row[1])
	return returning

#experimental for session control
def sumSessionCounter():
	try: 
		session['counter'] +=1
	except KeyError:
		session['counter'] = 1

'''
@login_manager.user_loader
def load_user(userid):
	return User.get(userid)'''


def connect_db():
		rv = lite.connect(app.config['DATABASE'])
		rv.row_factory = lite.Row
		return rv

def get_db():
		"""opens new database connection if there is none yet for the current application context"""
		if not hasattr(g, 'test_db'):
			g.test_db = connect_db()
		return g.test_db

@app.teardown_appcontext
def close_db(error):
		"""closes the db post request"""
		if hasattr(g, 'test_db'):
			g.test_db.close()

@app.before_request
def before_request():
		g.db = connect_db()

@app.route('/') #gets executed when the page is opened
def send_index():
			#return send_from_directory('static/static_html', 'test.html')
			#print storeUsers(usernameGenereator,passwordGenereator)
			user = usernameGenereator()
			userID = storeUsers(user, passwordGenereator())
			print str(userID)+"userid"
			sessionID = storeSession(userID, datetime.datetime.now(), datetime.datetime.now())
			questions = loadQandA()
			#return render_template('index.html', title = "Testform", answers = ans, questions = questions, size = len(questions))
			return render_template('index.html', title = nameOfTest, questions = questions, size = len(questions))

@app.route('/<path:path>') #initializes table as well
def send_static_html(path):
				return send_from_directory('static/static_html', path)

@app.route('/js/<path:path>') #loads javascript
def send_js(path):
		return send_from_directory('static/js', path)

@app.route('/css/<path:path>') #loads css
def send_css(path):
		return send_from_directory('static/css', path)

@app.route('/_savedata', methods=['GET', 'POST']) #saves the input from the forms into the database
def saveData():
		con = lite.connect('database.db')
		theuserid = ''
		thesessionid = ''
		with con:
			cur = con.cursor()
			cur.execute('SELECT max(UserID) FROM Users')
			theuserid = cur.fetchone()
			cur.execute('SELECT max(SessionID) FROM Sessions')
			thesessionid = cur.fetchone()
			theuserid = theuserid[0]
			thesessionid = thesessionid[0]
		thelist = request.get_json()
		questions = loadQandA()
		iterator = iter(questions)
		i = 0
		while i < len(questions):
				thisquest = iterator.next()
				indexofanswer = int(thelist[i])
				possibleanswers = questions[thisquest]
				thisans = possibleanswers[indexofanswer-1]
				storeAnswer(theuserid, thesessionid, thisquest, thisans)
				i = i + 1
		return jsonify(result = i)


if __name__ == "__main__":
				host_loc = "127.0.0.1"
				print "Running server at %s" % host_loc
				app.run(host=host_loc)