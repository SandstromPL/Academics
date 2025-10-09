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
    
try:
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