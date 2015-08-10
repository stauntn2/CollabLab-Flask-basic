import sqlite3 as lite
import sys
import datetime
import time
import json
con = lite.connect('database.db')
# foreign_keys = ON
def addToQs(new_question, new_answers):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Questions (Question, Answers) VALUES(?,?)", (new_question, json.dumps(new_answers)))


with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("DROP TABLE IF EXISTS Sessions")
    cur.execute("DROP TABLE IF EXISTS Answers")
    cur.execute("DROP TABLE IF EXISTS Questions")
    cur.execute("CREATE TABLE Users(UserID INTEGER PRIMARY KEY AUTOINCREMENT, AmazonID VARCHAR(25), Password VARCHAR(25) )") #3 columns
    cur.execute("CREATE TABLE Sessions(SessionID INTEGER PRIMARY KEY AUTOINCREMENT, UserID INT, Timebegan TIMESTAMP, Timeended TIMESTAMP, FOREIGN KEY(UserID) REFERENCES Users(UserID))") #4 columns
    cur.execute("CREATE TABLE Answers(AnswerID INTEGER PRIMARY KEY AUTOINCREMENT, UserID INT , SessionID INT , Question VARCHAR(255), Answer VARCHAR(100), FOREIGN KEY(UserID) REFERENCES Users(UserID), FOREIGN KEY(SessionID) REFERENCES Sessions(SessionID))") #5 columns
    cur.execute("CREATE TABLE Questions(QuestionID INTEGER PRIMARY KEY AUTOINCREMENT, Question VARCHAR(225), Answers VARCHAR(225))")

answers = ['bob','joe','max','sam']

addToQs('Who\'s the fastest?', answers)
addToQs('Who\'s the coolest?', answers)
addToQs('Who\'s the strongest?', ['jim','kevin','danny','jack'])
addToQs('Where are the pals?', ['pool','house','work', 'school','vacation','outdoors','at a sport'])
addToQs('How does this image make you feel?', ['happy', 'indifferent', 'sad' ])
addToQs('What if I were to tell you that this question is a test to see if the div heights adjusted in both directions and as a consequence there could only be one possible answer?', ['bad'])
addToQs("Alphabetical?",['yes','no','maybe so'])
addToQs("Should this additional question be here?", ['yes, it adds value', 'yes, it\'s cool','no, too much', 'no, too little' ])
