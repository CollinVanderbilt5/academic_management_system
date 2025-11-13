## A the file used for the MYsql database being hosted.
## This allows the database to be hosted onto a server that we can connect to.

## This file requires set up
## You need to install MySQL 8.44 if you want to see the database since it's hosted on a server
## use the host, user , and password to log in, you may need to give me your IP
## You also need to pip install mysql-connector-python
## Then your done!

import mysql.connector

db = mysql.connector.connect( ## Connects to the server
    host="whiteboard-db.czyckmoyq306.us-east-2.rds.amazonaws.com",
    user="admin",
    passwd="nerdherd17", ##This is whatever password you used for the server
    database="whiteboard"
)

cursor = db.cursor()


cursor.execute("Select * From Advisor")

print(cursor.fetchall())

db.close()