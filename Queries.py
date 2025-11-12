## An example of using MYsql, this allows the database to be hosted onto a server that we can connect to, though for now we're using local host

## This file requires set up
## You need to install MySQL
## Then make a local server with the user root and the password 1234
## Then you have to make a new database in mysql called Whiteboard
## You also need to pip install mysql-connector-python
##Then your done!

import mysql.connector

db = mysql.connector.connect( ## Connects to the server
    host="localhost",
    user="root",
    passwd="1234", ##This is whatever password you used for the server
    database="Whiteboard"
)

cursor = db.cursor()


cursor.execute("Select * From Advisor")

print(cursor.fetchall())

db.close()