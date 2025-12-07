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

    ## Set up connection
    connection = get_connection()
    if not connection:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    
    
    query = "SELECT name FROM Student WHERE student_id=%s AND password=%s"
    cursor.execute(query, (curr_id, password))
    current_user = cursor.fetchone()
    
    if current_user: ## If true, we got a Student, return info
        cursor.close()
        connection.close()
        return jsonify({"success": True, "User" : current_user['name'], "ID" : curr_id, "account_type" : "Student"})

    query = "SELECT name FROM Professor WHERE prof_id=%s AND password=%s"
    cursor.execute(query, (curr_id, password))
    current_user = cursor.fetchone()
    
    if current_user: ## If true, we got an Professor, return info
        cursor.close()
        connection.close()
        return jsonify({"success": True, "user" : current_user['name'], "id" : curr_id, "account_type" : "Professor"})
    

    query = "SELECT name FROM Advisor WHERE advisor_id=%s AND password=%s"
    cursor.execute(query, (curr_id, password))
    current_user = cursor.fetchone()
    
    if current_user: ## If true, we got a Advisor, return info
        cursor.close()
        connection.close()
        return jsonify({"success": True, "user" : current_user['name'], "id" : curr_id, "account_type" : "Advisor"})


    else:
        return jsonify({"success": False, "user" : current_user, "account_type" : "Null"})
    

def signUp(user, name, pwd):
    pass

## account type will be an enum, 0 = student, 1 = profesor, 2 =  advisor
def addUser(user_account_type : int, account_to_add_type : int, id, password):
    
    ## Makes it so accounts can't edit any accoint on a higher tier
    if account_to_add_type < user_account_type: 
        return jsonify({"success": False, "error" : "can't add account higher than your own"})
    
    connection = get_connection()
    if not connection:
        return jsonify({"success": False, "error": "DB connection failed"}), 500
    
    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    query = None

    match account_to_add_type:
        case 0:
            query = f"INSERT into Student({id}, NULL, NULL, NULL, {password})"
        case 1:
            query = f"INSERT into Professor({id}, NULL, NULL, NULL, NULL,{password})"
        case 2:
            query = f"INSERT into Advisor({id}, NULL, NULL, NULL, NULL,{password})"

    if query:
        cursor.execute(query)
    
    ## We just search for the user we added to see if the change worked
    match account_to_add_type:
        case 0:
            query = f"INSERT into Student({id}, NULL, NULL, NULL, {password})"
        case 1:
            query = f"INSERT into Professor({id}, NULL, NULL, NULL, NULL,{password})"
        case 2:
            query = f"INSERT into Advisor({id}, NULL, NULL, NULL, NULL,{password})"

    if query:
        cursor.execute(query)

    check = cursor.fetchone()

    ## If we found our person, return true
    if check:
        cursor.close()
        connection.close()
        return jsonify({"success" : True})
    else:
        return jsonify({"success": False, "error": "DB insertion failed"}), 500

## account type will be an enum, 0 = student, 1 = profesor, 2 =  advisor
def deleteUser(user_account_type : int, account_to_delete_type : int, id : int):
    
    ## Makes it so accounts can't edit any accoint on a higher tier
    if account_to_delete_type < user_account_type: 
        return jsonify({"success": False, "error" : "can't add account higher than your own"})

    connection = get_connection()
    if not connection:
        return jsonify({"error": "DB connection failed"}), 500
    
    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    
    if user_account_type == 0 : ##stuent account
        query = "DELETE FROM Student WHERE student_id=id"

    if user_account_type == 1 : ##professor account
        query = "DELETE FROM Professor WHERE prof_id=id"

    if user_account_type == 2 : ##advisor account
        query = "DELETE FROM Admin WHERE ad_id=id"

    cursor.execute(query)

    
    cursor.close()
    connection.close()
    

def enrollClass(advising_hold : bool, sid : int):
    
    pass

def dropClass(sid : int):
    pass

def addAsignment(id : int):
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

def editHold(user_account_type : int, id : int):
    pass


## only call this function if you're running this file, otherwise this is skipped
## This part opens the database and adds thing in the setup.sql file
if __name__ == "__main__":
    connection = get_connection()

    if not connection:
        Exception("Couldn't connect to database!")
    pass

    
