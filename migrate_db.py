import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create the table if it does not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        name TEXT NOT NULL,
        program TEXT NOT NULL,
        year INTEGER NOT NULL,
        section TEXT NOT NULL,
        source TEXT DEFAULT 'Local'
    )
""")

# Check existing columns
columns = [
    row[1]
    for row in cursor.execute(
        "PRAGMA table_info(students)"
    ).fetchall()
]

# Add source column if missing
if "source" not in columns:
    cursor.execute("""
        ALTER TABLE students
        ADD COLUMN source TEXT DEFAULT 'Local'
    """)

# Set existing records without a source to Local
cursor.execute("""
    UPDATE students
    SET source = 'Local'
    WHERE source IS NULL OR source = ''
""")

conn.commit()
conn.close()

print("Database migration completed successfully.")
print("Source column is ready.")
print("Existing student records were preserved.")