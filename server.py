import mysql.connector
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS


## This file is using a virtual environment within the code base
## Since the enviorment is already made just type 'my_project_env\Scripts\activate' into the terminal to activate it
## If you want to see the libraries installed, just check requirements.txt


app = Flask(__name__)
app.secret_key = "your-secret-key"
CORS(app)  # Allows JS from another domain to call your API


##-----------DATA BASE QUERY FUNCTIONS-----------##
## We might move this into another file

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
    return render_template("index.html")

@app.route('/addremove.html')
def addremove():
    return render_template("addremove.html")

@app.route('/addassignment.html')
def addassign():
    return render_template("addassignment.html")

@app.route('/advisinghold.html')
def advishold():
    return render_template("advisinghold.html")

@app.route('/calendar.html')
def calender():
    return render_template("calendar.html")

@app.route('/enrolldrop.html')
def enroll():
    return render_template("enrolldrop.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)