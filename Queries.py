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
        return jsonify({"success": True, "user" : current_user['name'], "ID" : curr_id, "account_type" : "Student"})

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
        cursor.close()
        connection.close()
        return jsonify({"success": False, "user" : current_user, "account_type" : "Null"})

## account type will be an enum, 0 = student, 1 = profesor, 2 =  advisor
def addUser(user_account_type : int, account_to_add_type : int, id, password : str):
    
    ## Makes it so accounts can't edit any accoint on a higher tier
    if account_to_add_type > user_account_type: 
        return jsonify({"success": False, "error" : "can't add account higher than your own"})
    
    connection = get_connection()
    if not connection:
        return jsonify({"success": False, "error": "DB connection failed"}), 500
    
    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    query = None


    ## First check if the account already exist
    match account_to_add_type:
        case 0:
           query = f"SELECT * FROM Student WHERE student_id={id};"
        case 1:
            query = f"SELECT * FROM Student WHERE student_id={id}"
        case 2:
            query = f"SELECT * FROM Student WHERE student_id={id}"

    if query:
        cursor.execute(query)

    check = cursor.fetchone()

    if check:
        cursor.close()
        connection.close()
        return jsonify({"success": False, "error": "User ID Already exists"})
        
    match account_to_add_type:
        case 0:
            query = f"INSERT into Student (student_id, password) Values({id}, \"{password}\")"
        case 1:
            query = f"INSERT into Professor (prof_id, password) Values({id} ,\"{password}\")"
        case 2:
            query = f"INSERT into Advisor (advisor_id, password) Values({id},\"{password}\")"

    if query:
        cursor.execute(query)
        connection.commit()
    
    ## We just search for the user we added to see if the change worked
    match account_to_add_type:
        case 0:
           query = f"SELECT * FROM Student WHERE student_id={id} AND password=\"{password}\";"
        case 1:
            query = f"SELECT * FROM Student WHERE student_id={id} AND password=\"{password}\""
        case 2:
            query = f"SELECT * FROM Student WHERE student_id={id} AND password=\"{password}\""

    if query:
        cursor.execute(query)

    check = cursor.fetchone()

    ## If we found our person, return true
    if check:
        cursor.close()
        connection.close()
        return jsonify({"success" : True})
    else:
        cursor.close()
        connection.close()
        return jsonify({"success": False, "error": "DB insertion failed"}), 500
    
    

## account type will be an enum, 0 = student, 1 = profesor, 2 =  advisor
def deleteUser(user_account_type : int, account_to_delete_type : int, id : int):
    
    ## Makes it so accounts can't edit any accoint on a higher tier
    if account_to_delete_type > user_account_type: 
        return jsonify({"success": False, "error" : "can't add account higher than your own"})

    connection = get_connection()
    if not connection:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    
    ## First check if the account already exist
    match account_to_delete_type:
        case 0:
           query = f"SELECT * FROM Student WHERE student_id={id};"
        case 1:
            query = f"SELECT * FROM Student WHERE student_id={id}"
        case 2:
            query = f"SELECT * FROM Student WHERE student_id={id}"

    if query:
        cursor.execute(query)
    check = cursor.fetchone()

    if check == None:
        cursor.close()
        connection.close()
        return jsonify({"success": False, "error": "ID doesn't exists"})
    
    match account_to_delete_type:
        case 0:
            query = f"DELETE FROM Student WHERE student_id={id}"
        case 1:
            query = f"DELETE FROM Professor WHERE prof_id={id}"
        case 2:
            query = f"DELETE FROM Admin WHERE ad_id={id}"

    cursor.execute(query)
    connection.commit()

    ## We just search for the user we added to see if the change worked
    match account_to_delete_type:
        case 0:
            query = f"SELECT * FROM Student WHERE student_id={id}"
        case 1:
            query = f"SELECT * FROM Student WHERE student_id={id}"
        case 2:
            query = f"SELECT * FROM Student WHERE student_id={id}"

    if query:
        cursor.execute(query)

    check = cursor.fetchone()

    ## If we found our person, return false since it didn't work
    if check:
        cursor.close()
        connection.close()
        return jsonify({"success" : False, "error": "DB deletion failed"}), 500
    else:
        cursor.close()
        connection.close()
        return jsonify({"success": True})

def enrollClass(advising_hold : bool, sid : int):
    connection = get_connection()
    if not connection:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = connection.cursor()

    course_id_input = input("Enter the course ID: ")

    if advising_hold:
        return jsonify({"success": False, "message" : "Unable to enroll due to advising hold", "sid" : sid}), 500
    else:
        query = "SELECT course_id FROM Class WHERE course_id=%s"
        cursor.execute(query, (course_id_input,))
        course_exist = cursor.fetchone()
    
        if course_exist:
            query_insert = "INSERT INTO Is_in VALUES(sid, course_id, 100)"
            cursor.execute(query_insert)
            cursor.commit()
            return jsonify({"success": True, "course_id" : course_id_input, "sid" : sid})
        else:
            return jsonify({"success": False, "message" : "Course does not exist", "course_id" : course_id_input}), 500
    cursor.close()
    connection.close()
    pass

def dropClass(sid : int):
    connection = get_connection()
    if not connection:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = connection.cursor()

    course_id_input = input("Enter the course ID: ")

    query = "SELECT course_id FROM Class WHERE course_id=%s"
    cursor.execute(query, (course_id_input,))
    course_exist = cursor.fetchone()

    if course_exist:
        query_drop = "DELETE FROM Is_in WHERE course_id_input=course_id"
        cursor.execute(query_drop)
        cursor.commit()
        return jsonify({"success": True, "course_id" : course_id_input, "sid" : sid})
    else:
        return jsonify({"success": False, "message" : "Course does not exist", "course_id" : course_id_input}), 500
    cursor.close()
    connection.close()
    pass



def add_assignment(course_id, title, description, point_value, due_date, type_, duration=None, room=None, partners=None):
    connection = get_connection()
    if not connection:
        return {"success": False, "error": "DB connection failed"}
    cursor = connection.cursor()

    try:
        # Insert into Assignment table
        query = """
            INSERT INTO Assignment (course_id, title, point_value, grade, description, due_date, completed)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (course_id, title, point_value, 0, description, due_date, False))

        # Insert into type-specific tables
        if type_ == "Quiz" and duration is not None:
            cursor.execute("INSERT INTO Quiz (course_id, title, duration) VALUES (%s, %s, %s)", 
                           (course_id, title, duration))
        elif type_ == "Exam" and room is not None:
            cursor.execute("INSERT INTO Exam (course_id, title, room) VALUES (%s, %s, %s)",
                           (course_id, title, room))
        elif type_ == "Project" and partners is not None:
            cursor.execute("INSERT INTO Project (course_id, title, partners) VALUES (%s, %s, %s)",
                           (course_id, title, partners))

        connection.commit()
        return {"success": True}
    except Exception as e:
        print("Error adding assignment:", e)
        connection.rollback()
        return {"success": False, "error": str(e)}
    finally:
        cursor.close()
        connection.close()




def organizeByDueDates():
    pass

def organizeByClass():
    pass

def checkOffCheck():
    pass

def searchForAssignment():
    connection = get_connection()
    if not connection:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names

    assignment_name = input("Enter assignment name to search for: ")
    course_id = input("Enter course ID to search in: ")
    due_date : str
    point_value : int
    class_title : str

    connection = get_connection()
    if not connection:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    
    query = "SELECT course_id, due_date, point_value INTO @course_id, @due_date, @point_value  FROM Assignment WHERE name=%s AND course_id=%s"
    cursor.execute(query, (assignment_name, course_id))
    assignment = cursor.fetchone()

    if assignment:
        cursor.close()
        connection.close()
        print(assignment_name, due_date, point_value, class_title, sep=', ', end='end')
        return jsonify({"success": True, "assignment_name" : assignment_name, "course_id" : assignment['course_id'], "due_date" : assignment['due_date'], "point_value" : assignment['point_value'], "class_title" : class_title})


    else:
        return jsonify({"success": False, "error" : "assignment not found"})
    pass

def editHold(user_account_type : int, student_id : int):

    connection = get_connection()
    if not connection:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names

    if user_account_type != 2: ##only advisors can edit holds
        return jsonify({"success": False, "error" : "can't edit holds with your account type"})

    ##Checks if the student exist
    query = f"SELECT name FROM Student WHERE student_id={student_id}"
    cursor.execute(query)
    fetch_check = cursor.fetchone()
    if not fetch_check:
        return jsonify({"success": False, "error" : "student not found"})

    query = f"select advising_hold from Student WHERE student_id={student_id}"
    cursor.execute(query)

    fetch_check = cursor.fetchone()
    ##update the student advising hold
    query = f"UPDATE Student SET advising_hold = NOT advising_hold WHERE student_id={student_id}"
    cursor.execute(query)
    cursor.close()
    connection.close()
    return getAdvisingHold(student_id)
    # else:
    #     return jsonify({"success": False, "error" : "invalid account type"})

    # return jsonify({"success": True, "message" : "hold status updated"})
 
def getAdvisingHold(student_id: int):
    connection = get_connection()
    if not connection:
        return {"success": False, "error": "DB connection failed"}

    cursor = connection.cursor(dictionary=True)
    query = f"SELECT advising_hold FROM Student WHERE student_id={student_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result is None:
        return {"success": False, "error": "Student not found"}
    else:
        return {"success": True, "advising_hold": bool(result["advising_hold"])}


# For calendar view: gets all assignments
def get_all_assignments():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Assignment ORDER BY due_date ASC")
        rows = cursor.fetchall() 

        cursor.close()
        conn.close()
        return rows
    except mysql.connector.Error as err:
        print("Error:", err)
        return []

def get_all_assignments_json():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Pull assignments from Assignment table, join Class to get course title
        cursor.execute("""
            SELECT a.course_id, c.title AS course_title, a.title AS assignment_title, 
                   a.point_value, a.due_date, a.completed
            FROM Assignment a
            JOIN Class c ON a.course_id = c.course_id
            ORDER BY a.due_date ASC
        """)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({"success": True, "assignments": rows})

    except mysql.connector.Error as err:
        print("Error fetching assignments:", err)
        return jsonify({"success": False, "assignments": [], "error": str(err)})

## only call this function if you're running this file, otherwise this is skipped
## This part opens the database and adds thing in the setup.sql file
if __name__ == "__main__":
    connection = get_connection()

    if not connection:
        Exception("Couldn't connect to database!")
    
    print("\"Hi\"")

    
