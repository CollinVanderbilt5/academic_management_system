import mysql.connector
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from Queries import *

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


##------------ Website Routes ------------##
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def userLogin():
    data = request.get_json()
    return login(data.get("username"), data.get("password"))

@app.route('/adduser', methods=['POST'])
def add_user():
    data = request.get_json()
    return addUser(data.get("account_type"), data.get("add_type"), data.get("add_id"), data.get("add_pass"))

@app.route('/removeuser', methods=['POST'])
def remove_user():
    data = request.get_json()
    return deleteUser(data.get("account_type"), data.get("add_type"), data.get("add_id"))

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

# Add assignment to database
@app.route("/api/add_assignment", methods=["POST"])
def api_add_assignment():
    data = request.json
    course_id = data.get("course_id")
    title = data.get("title")
    description = data.get("description", "")
    point_value = data.get("point_value", 0)
    due_date = data.get("due_date")
    type_ = data.get("type")
    duration = data.get("duration")
    room = data.get("room")
    partners = data.get("partners")

    result = add_assignment(course_id, title, description, point_value, due_date, type_, duration, room, partners)
    return jsonify(result)


@app.route('/advisinghold.html')
def advishold():
    return render_template("advisinghold.html")

@app.route('/calendar.html')
def calender():
    return render_template("calendar.html")

@app.route("/api/get_assignments", methods=["POST"])
def get_assignments_route():
    data = request.json
    id = data.get("id")
    sortDate = data.get("datesort")
    sortClass = data.get("classsort")
    return get_all_assignments_json(id, sortDate or sortClass, sortDate)

@app.route('/enrolldrop.html')
def enroll():
    return render_template("enrolldrop.html")

@app.route("/api/enroll_class", methods=["POST"])
def api_enroll_class():
    data = request.get_json()
    success = enrollClass(data["student_id"], data["course_id"]) 
    return jsonify({"success": success})

@app.route("/api/drop_class", methods=["POST"])
def api_drop_class():
    data = request.get_json()
    success = enrollClass(data["student_id"], data["course_id"]) 
    return jsonify({"success": success})

@app.route("/api/get_hold", methods=["POST"])
def api_get_hold():
    data = request.get_json()
    student_id = data.get("student_id")
    if not student_id:
        return jsonify({"success": False, "error": "Student ID missing"})
    
    result = getAdvisingHold(student_id)
    return jsonify(result)

@app.route("/api/edit_hold", methods=["POST"])
def api_edit_hold():
    data = request.get_json()
    student_id = data.get("student_id")
    # TODO: Replace 2 with actual logged-in advisor type check if needed
    result = editHold(user_account_type=2, student_id=student_id)
    if result is None:  # your current editHold doesn't return anything
        # We can fetch the new value
        result = getAdvisingHold(student_id)
    return jsonify({"success": True, "advising_hold": result.get("advising_hold")})

@app.route("/api/complete_assignment", methods=["POST"])
def complete_assignment():
    data = request.get_json()
    course_id = data.get("course_id")
    title = data.get("title")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE Assignment SET completed = TRUE WHERE course_id = %s AND title = %s"
        cursor.execute(query, (course_id, title))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(port=5000, debug=True)