import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows JS from another domain to call your API

db = mysql.connector.connect( ## Connects to the server
    host="whiteboard-db.czyckmoyq306.us-east-2.rds.amazonaws.com",
    user="admin",
    passwd="nerdherd17", ##This is whatever password you used for the server
    database="whiteboard"
)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Python!"})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")


    try:
        conn = mysql.connector.connect(db)
        cursor = conn.cursor(dictionary=True)  # dictionary=True gives column names
        query = "SELECT name FROM Student WHERE student_id=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
    except mysql.connector.Error as err:
        return jsonify({"success": False, "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


    if user:
        return jsonify({"success": True, "User" : user})



if __name__ == '__main__':
    app.run(port=5000, debug=True)