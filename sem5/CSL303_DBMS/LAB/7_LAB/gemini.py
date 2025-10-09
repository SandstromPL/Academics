import sqlite3
import time
import random
import os

# --- Configuration ---
DB_FILE = "university.db"
SELECT_ITERATIONS = 100
INSERT_COUNT = 500
SELECT_QUERY = "SELECT * FROM Students WHERE major = 'Computer Science';"

# Ensure the database file exists before proceeding
if not os.path.exists(DB_FILE):
    print(f"Error: Database file '{DB_FILE}' not found.")
    print("Please create and populate it as per Part 1 of the lab instructions.")
    exit()

# --- Part 3, Questions 12 & 13: SELECT Performance ---

print("--- Measuring SELECT Performance ---")

# Question 12: Measure SELECT time WITHOUT index
try:
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        # Drop the index to measure baseline performance
        try:
            cur.execute("DROP INDEX idx_students_major")
            print("Index 'idx_students_major' dropped for baseline measurement.")
        except sqlite3.OperationalError:
            print("Index 'idx_students_major' did not exist. Measuring baseline.")

        total_time_no_index = 0
        for _ in range(SELECT_ITERATIONS):
            start_time = time.perf_counter()
            cur.execute(SELECT_QUERY).fetchall()
            end_time = time.perf_counter()
            total_time_no_index += (end_time - start_time)

        avg_time_no_index = total_time_no_index / SELECT_ITERATIONS
        print(f"[Question 12] Avg. time without index: {avg_time_no_index:.6f} seconds")

# Question 13: Measure SELECT time WITH index
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        # Create the index to measure improved performance
        print("\nRe-creating index 'idx_students_major'...")
        cur.execute("CREATE INDEX idx_students_major ON Students (major);")

        total_time_with_index = 0
        for _ in range(SELECT_ITERATIONS):
            start_time = time.perf_counter()
            cur.execute(SELECT_QUERY).fetchall()
            end_time = time.perf_counter()
            total_time_with_index += (end_time - start_time)

        avg_time_with_index = total_time_with_index / SELECT_ITERATIONS
        print(f"[Question 13] Avg. time with index:    {avg_time_with_index:.6f} seconds")
        print("-" * 35)

except Exception as e:
    print(f"An error occurred during SELECT tests: {e}")


# --- Part 3, Questions 14 & 15: INSERT Performance ---

print("\n--- Measuring INSERT Performance ---")

# Generate 500 random enrollments to insert
# Note: Assumes 2000 students (IDs 1-2000) and 100 courses (IDs 1-100)
enrollment_data = []
for _ in range(INSERT_COUNT):
    student_id = random.randint(1, 2000)
    course_id = random.randint(1, 100)
    grade = round(random.uniform(50.0, 100.0), 2)
    enrollment_data.append((student_id, course_id, grade))

# Question 14: Measure INSERT time WITH indexes
try:
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        # Ensure the foreign key indexes exist
        print("Creating foreign key indexes on Enrollments table...")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_enrollments_student_id ON Enrollments (student_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_enrollments_course_id ON Enrollments (course_id);")
        
        start_time = time.perf_counter()
        # Using executemany is the standard way to perform bulk inserts
        cur.executemany("INSERT INTO Enrollments (student_id, course_id, grade) VALUES (?, ?, ?)", enrollment_data)
        con.commit() # Commit the transaction
        end_time = time.perf_counter()
        
        time_with_indexes = end_time - start_time
        print(f"[Question 14] Time to insert {INSERT_COUNT} records with indexes: {time_with_indexes:.6f} seconds")

# Question 15: Measure INSERT time WITHOUT indexes
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        # Drop the foreign key indexes
        print("\nDropping foreign key indexes from Enrollments table...")
        cur.execute("DROP INDEX idx_enrollments_student_id;")
        cur.execute("DROP INDEX idx_enrollments_course_id;")

        # Important: We must delete the previously inserted data to ensure a fair comparison
        cur.execute("DELETE FROM Enrollments WHERE enrollment_id > 10000;")
        con.commit()

        start_time = time.perf_counter()
        cur.executemany("INSERT INTO Enrollments (student_id, course_id, grade) VALUES (?, ?, ?)", enrollment_data)
        con.commit()
        end_time = time.perf_counter()

        time_without_indexes = end_time - start_time
        print(f"[Question 15] Time to insert {INSERT_COUNT} records without indexes: {time_without_indexes:.6f} seconds")
        print("-" * 35)

except Exception as e:
    print(f"An error occurred during INSERT tests: {e}")
