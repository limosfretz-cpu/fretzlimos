import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# EXISTING STUDENT ENDPOINT
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00103",
        "name": "Fretz Limos",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })


# EXISTING GREETING ENDPOINT
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


# DATABASE ENDPOINT: ALL STUDENTS
@app.route('/students')
def get_students():
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# DATABASE ENDPOINT: STUDENT BY DATABASE ID
@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(dict(student))


# CUSTOM ENDPOINT 1: CAMPUS EVENTS
@app.route('/campus-events')
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


# CUSTOM ENDPOINT 2: COURSE INFORMATION
@app.route('/course-info/<course_code>')
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

    course = courses.get(course_code.upper())

    if course:
        return jsonify({
            "course_code": course_code.upper(),
            "course_information": course
        })

    return jsonify({
        "error": "Course not found",
        "course_code": course_code.upper()
    }), 404


if __name__ == '__main__':
    app.run(debug=True)