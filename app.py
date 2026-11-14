import sqlite3
import requests

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

DATABASE = "students.db"

# Partner's deployed API endpoint
PARTNER_URL = "https://jarellkrismagarso-1.onrender.com/api/students"


# =========================================
# DATABASE CONNECTION
# =========================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================
# STUDENT INFORMATION
# =========================================

@app.route("/student")
def get_student():
    return jsonify({
        "student_id": "24-00103",
        "name": "Fretz Limos",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })


# =========================================
# GREETING API
# =========================================

@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Student")

    return jsonify({
        "message": f"Hello, {name}!"
    })


# =========================================
# CAMPUS EVENTS
# =========================================

@app.route("/campus-events")
def get_campus_events():
    return jsonify({
        "events": [
            {
                "event_id": 1,
                "event_name": "IT Skills Workshop",
                "date": "2026-11-20",
                "venue": "Computer Laboratory",
                "status": "Upcoming"
            },
            {
                "event_id": 2,
                "event_name": "Programming Competition",
                "date": "2026-11-25",
                "venue": "ISUFST Auditorium",
                "status": "Upcoming"
            },
            {
                "event_id": 3,
                "event_name": "Student Technology Seminar",
                "date": "2026-12-05",
                "venue": "University Function Hall",
                "status": "Upcoming"
            }
        ]
    })


# =========================================
# COURSE INFORMATION
# =========================================

@app.route("/course-info/<course_code>")
def get_course_info(course_code):
    courses = {
        "IT101": {
            "course_name": "Introduction to Computing",
            "units": 3,
            "department": "Information Technology"
        },
        "IT202": {
            "course_name": "Database Management Systems",
            "units": 3,
            "department": "Information Technology"
        },
        "IT303": {
            "course_name": "Web Development",
            "units": 3,
            "department": "Information Technology"
        }
    }

    course_code = course_code.upper()
    course = courses.get(course_code)

    if course:
        return jsonify({
            "course_code": course_code,
            "course_information": course
        })

    return jsonify({
        "error": "Course not found",
        "course_code": course_code
    }), 404


# =========================================
# GET ALL LOCAL STUDENTS
# =========================================

@app.route("/students")
def get_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# =========================================
# GET LOCAL STUDENT BY DATABASE ID
# =========================================

@app.route("/students/<int:id>")
def get_student_by_id(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(dict(student))


# =========================================
# GET ALL STUDENTS THROUGH API
# =========================================

@app.route("/api/students", methods=["GET"])
def api_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# =========================================
# STEP 8: RECEIVE EXTERNAL STUDENT RECORD
# =========================================

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required"
        }), 400

    required_fields = [
        "student_id",
        "name",
        "program",
        "year",
        "section"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    source = data.get("source", "External API")

    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO students
            (student_id, name, program, year, section, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["student_id"],
                data["name"],
                data["program"],
                data["year"],
                data["section"],
                source
            )
        )

        conn.commit()

        return jsonify({
            "message": "Student added successfully",
            "id": cursor.lastrowid,
            "student_id": data["student_id"],
            "source": source
        }), 201

    except sqlite3.Error as error:
        conn.rollback()

        return jsonify({
            "error": "Unable to save student",
            "details": str(error)
        }), 500

    finally:
        conn.close()


# =========================================
# GET STUDENT THROUGH API BY ID
# =========================================

@app.route("/api/students/<int:id>", methods=["GET"])
def api_get_student(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(dict(student))


# =========================================
# UPDATE STUDENT
# =========================================

@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required"
        }), 400

    required_fields = [
        "student_id",
        "name",
        "program",
        "year",
        "section"
    ]

    if not all(field in data for field in required_fields):
        return jsonify({
            "error": "Missing required student information"
        }), 400

    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            UPDATE students
            SET student_id = ?,
                name = ?,
                program = ?,
                year = ?,
                section = ?
            WHERE id = ?
            """,
            (
                data["student_id"],
                data["name"],
                data["program"],
                data["year"],
                data["section"],
                id
            )
        )

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Student not found"
            }), 404

        return jsonify({
            "message": "Student updated successfully"
        })

    except sqlite3.Error as error:
        conn.rollback()

        return jsonify({
            "error": "Unable to update student",
            "details": str(error)
        }), 500

    finally:
        conn.close()


# =========================================
# DELETE STUDENT
# =========================================

@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (id,)
        )

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Student not found"
            }), 404

        return jsonify({
            "message": "Student deleted successfully"
        })

    except sqlite3.Error as error:
        conn.rollback()

        return jsonify({
            "error": "Unable to delete student",
            "details": str(error)
        }), 500

    finally:
        conn.close()


# =========================================
# RETRIEVE PARTNER RECORDS
# =========================================

@app.route("/partner-records")
def partner_records():
    try:
        response = requests.get(
            PARTNER_URL,
            timeout=30
        )

        response.raise_for_status()

        records = response.json()

        if not isinstance(records, list):
            return jsonify({
                "error": "Partner API did not return a list of records"
            }), 502

        return jsonify(records)

    except requests.RequestException as error:
        return jsonify({
            "error": "Unable to retrieve partner records",
            "details": str(error)
        }), 502

    except ValueError:
        return jsonify({
            "error": "Partner API returned invalid JSON"
        }), 502


# =========================================
# IMPORT PARTNER RECORD INTO LOCAL DATABASE
# =========================================

@app.route("/import-student", methods=["POST"])
def import_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required"
        }), 400

    required_fields = [
        "student_id",
        "name",
        "program",
        "year",
        "section"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO students
            (student_id, name, program, year, section, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["student_id"],
                data["name"],
                data["program"],
                data["year"],
                data["section"],
                "Classmate API"
            )
        )

        conn.commit()

        return jsonify({
            "message": "Partner record saved successfully",
            "id": cursor.lastrowid,
            "source": "Classmate API"
        }), 201

    except sqlite3.Error as error:
        conn.rollback()

        return jsonify({
            "error": "Unable to import partner record",
            "details": str(error)
        }), 500

    finally:
        conn.close()


# =========================================
# STEP 9: SEND PRACTICE RECORD TO PARTNER
# =========================================

@app.route("/send-practice-record", methods=["POST"])
def send_practice_record():
    record = {
        "student_id": "EXT-001",
        "name": "Sample Exchange Record",
        "program": "BSIT",
        "year": 1,
        "section": "A",
        "source": "Partner API"
    }

    try:
        response = requests.post(
            PARTNER_URL,
            json=record,
            timeout=30
        )

        try:
            partner_response = response.json()
        except ValueError:
            partner_response = response.text

        return jsonify({
            "message": "Practice record sent to partner",
            "status_code": response.status_code,
            "partner_response": partner_response
        }), response.status_code

    except requests.RequestException as error:
        return jsonify({
            "error": "Unable to send practice record",
            "details": str(error)
        }), 502


# =========================================
# INTEGRATION DASHBOARD STATISTICS
# =========================================

@app.route("/integration-stats")
def integration_stats():
    conn = get_db_connection()

    try:
        local_count = conn.execute("""
            SELECT COUNT(*) AS total
            FROM students
            WHERE source = 'Local'
               OR source IS NULL
               OR source = ''
        """).fetchone()["total"]

        imported_count = conn.execute("""
            SELECT COUNT(*) AS total
            FROM students
            WHERE source IS NOT NULL
              AND source != ''
              AND source != 'Local'
        """).fetchone()["total"]

        return jsonify({
            "local_records": local_count,
            "imported_records": imported_count
        })

    finally:
        conn.close()


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":
    app.run(debug=True)