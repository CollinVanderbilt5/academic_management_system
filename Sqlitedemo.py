## An example of using sqlite 3 and having a our database on the same system
import _sqlite3 ##<-- This is a built in library

connection = _sqlite3.connect('database/Whiteboard.db') ##Make/Open path to where the database will be, folder needs to be there

cursor = connection.cursor() ##The Cursor is how we interact with the database

sql_file = "setup.sql"
with open(sql_file, 'r') as f:
    sql_script = f.read()

    cursor.executescript(sql_script) ##This just makes the database from the setup file, easier this way
    connection.commit()

cursor.execute("Select * From Advisor") ##We use execute to do sql queries, it works for create table as well

print(cursor.fetchall()) ##We get the result as an array, here I'm just printing it

connection.close() ##must always close the database when we're done with it
