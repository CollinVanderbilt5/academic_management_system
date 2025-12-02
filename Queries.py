## A the file used to query, insert, and change values into the database.

## You need to install MySQL 8.44 if you want to see the database in a workbench
## use the host, user, and password to log in, you can also use localhost to test on your machine.
## If you're using localhost, run this file first, then run server.py

import mysql.connector
from flask import jsonify

def get_connection():
    db = mysql.connector.connect( ## Connects to the server
        host="whiteboard-db.czyckmoyq306.us-east-2.rds.amazonaws.com",
        user="admin",
        passwd="nerdherd17", ##This is whatever password you used for the server
        database="whiteboard"
    )
    if db:
        return db
    else:
        return None

## Takes ID, and Password. Searches database, returns a json filled with information of found table
def login(id, pwd):
    curr_id = id
    password = pwd

    connection = get_connection()

    if not connection:
        return jsonify({"error": "DB connection failed"}), 500

    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    query = "SELECT name FROM Student WHERE student_id=%s AND password=%s"
    cursor.execute(query, (curr_id, password))
    current_user = cursor.fetchone()
 
    cursor.close()
    connection.close()
    
    if current_user:
        return jsonify({"success": True, "User" : current_user['name'], "ID" : curr_id})
    else:
        return jsonify({"success": False, "User" : current_user})
    

def signUp(user, name, pwd):
    pass

def addUser():
    pass

def deleteUser(user_account_type : int, id : int):
    connection = get_connection()


    if not connection:
        return jsonify({"error": "DB connection failed"}), 500


    cursor = connection.cursor(dictionary=True)


    if user_account_type == 0 :
        query = f"DELETE FROM Students WHERE student_id={id}"
    elif user_account_type == 1 :
        query = f"DELETE FROM Professors WHERE prof_id={id}"
    elif user_account_type == 2 :
        query = f"DELETE FROM Advisors WHERE ad_id={id}"
    else:
        return jsonify({"error": "Invalid account type"}), 500


    cursor.execute(query)


    cursor.close()
    connection.close()
    pass

def enrollClass():
    pass

def dropClass():
    pass

def addAsignment():
    pass

def organizeByDueDates():
    pass

def organizeByClass():
    pass

def highlightAssignment():
    pass

def checkOffCheck():
    pass

def searchForAssignment():
    pass

def editHold():
    pass


## only call this function if you're running this file, otherwise this is skipped
## This part opens the database and adds thing in the setup.sql file
if __name__ == "__main__":
    connection = get_connection()

    if not connection:
        Exception("Couldn't connect to database!")
    pass

    
