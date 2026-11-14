import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
''')

# Remove previous sample records
cursor.execute("DELETE FROM students")

# Five sample student records
students = [
    ('26-01204', 'Rea Fe Sobejano', 'BSOA', 1, 'A'),
    ('24-00137', 'Jay Cris Encajonado', 'BSIT', 3, 'B'),
    ('24-00138', 'Jarell Kris Magarso', 'BSIT', 3, 'B'),
    ('25-00421', 'Maria Santos', 'BSIT', 2, 'A'),
    ('26-00815', 'Daniel Reyes', 'BSCS', 1, 'C')
]

cursor.executemany('''
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
''', students)

conn.commit()
conn.close()

print("Database created successfully.")