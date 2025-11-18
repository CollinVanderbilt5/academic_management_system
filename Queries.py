## A the file used for the MYsql database being hosted.
## This allows the database to be hosted onto a server that we can connect to.
## You need to install MySQL 8.44 if you want to see the database in a workbench
## use the host, user, and password to log in.

## This file requires 1 line of code
## In the terminal pip install mysql-connector-python
## This way you can test your code before putting it in server.py since it is large

import os
import mysql.connector

advisor : bool = False
student : bool = False
professor : bool = False

user : dict

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

def login(user, pwd) -> bool:
    conn = get_connection()
    if not conn:
        print("Sorry can't connect to database")
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM Student WHERE student_id=%s AND password=%s"
    cursor.execute(query, (user, pwd))
    user = cursor.fetchone()

    if user:
        student = True
        print("Welcome!", user["name"])
        return True
    else:
        query = "SELECT advisor_id FROM Advisor WHERE advisor_id=%s AND password=%s"
        cursor.execute(query, (user, pwd))
        user = cursor.fetchone()

    if user and not student: 
        advisor = True
        return True
    
    return False
    

def signUp(user, name, pwd):
    pass



running = True

login_screen : bool = True
dashboard : bool = False

while running:
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')
    

    if login_screen:
        print("Welcome to Whiteboard!")
        input_char = 'w'

        while input_char != 'l' and input_char != 's' and input_char != 'q':
            input_char = input("L to login, S to sign up, Q to quit: ")
        input_char = input_char.lower()

        if input_char == 'l':
            success : bool = False
            while (not success):
                user_nam = input("Username: ")
                passw = input("Password: ")
                success = login(user_nam, passw)

            
            running = False

        elif input_char == 's':
            
            running = False
        elif input_char == 'q':
            running = False



print("\nThanks for using Whiteboard!")
