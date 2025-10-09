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
        
except Exception as e:
    print(f"An error occurred during SELECT tests: {e}")