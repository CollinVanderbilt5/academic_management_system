import mysql.connector
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)  # Allows JS from another domain to call your API

current_user : dict

##-----------DATA BASE QUERY FUNCTIONS-----------##

## Get's the connection to the mySQL database (hosted via AWS)
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

## Returns user data if ID and password exist in the database
def login(id, pwd):
    id = id
    password = pwd

    connection = get_connection()

    if not connection:
        return jsonify({"error": "DB connection failed"}), 500

    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    query = "SELECT name FROM Student WHERE student_id=%s AND password=%s"
    cursor.execute(query, (id, password))
    user = cursor.fetchone()
 
    cursor.close()
    connection.close()


    if user:
        return jsonify({"success": True, "User" : user})
    else:
        return jsonify({"success": False, "User" : user})







##------------ Website Routes ------------##
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def userLogin():
    data = request.get_json()
    return login(data.get("username"), data.get("password"))

@app.route('/homepage')
def homepage():
    return render_template("homepage.html")

@app.route('/index.html')
def index():
    return render_template("homepage.html")

@app.route('/addremove.html')
def addremove():
    return render_template("addremove.html")

@app.route('/addassignment.html')
def addassign():
    return render_template("addassignment.html")

@app.route('/advisinghold.html')
def advishold():
    return render_template("advisinghold.html")

@app.route('/calender.html')
def calender():
    return render_template("calender.html")

@app.route('/enrolldrop.html')
def enroll():
    return render_template("enrolldrop.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)