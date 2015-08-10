import sqlite3 as lite
import sys


con = lite.connect('database.db')

with con:    
    cur = con.cursor()    
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        print row

    cur = con.cursor()    
    cur.execute("SELECT * FROM Sessions")
    rows = cur.fetchall()
    for row in rows:
        print row

    cur = con.cursor()    
    cur.execute("SELECT * FROM Answers")
    rows = cur.fetchall()
    for row in rows:
        print row