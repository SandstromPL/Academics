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

