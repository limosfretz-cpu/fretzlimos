
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00103",
        "name": "Fretz Limos",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


# NEW ENDPOINT 1: Campus Events
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


# NEW ENDPOINT 2: Course Information
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
