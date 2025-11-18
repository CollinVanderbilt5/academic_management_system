import mysql.connector
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows JS from another domain to call your API

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


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Python!"})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    connection = get_connection()

    if not connection:
        return jsonify({"error": "DB connection failed"}), 500

    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    query = "SELECT name FROM Student WHERE student_id=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
 
    cursor.close()
    connection.close()


    if user:
        return jsonify({"success": True, "User" : user})
    else:
        return jsonify({"success": False, "User" : user})



if __name__ == '__main__':
    app.run(port=5000, debug=True)