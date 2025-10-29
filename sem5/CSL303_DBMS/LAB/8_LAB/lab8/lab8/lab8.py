import psycopg2

# Database connection setup
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="studentdb",
            user="postgres",
            password="admin123"
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

# Task 1: Table creation
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                department VARCHAR(50)
            );
        """)
        conn.commit()
        print("Table 'Students' created successfully.")
        cursor.close()
    except Exception as e:
        print("Error creating table:", e)

# Task 2: Insert data
def insert_student(conn):
    try:
        cursor = conn.cursor()
        n = int(input("Enter number of students to insert: "))
        for _ in range(n):
            name = input("Name: ")
            age = int(input("Age: "))
            dept = input("Department: ")
            cursor.execute(
                "INSERT INTO Students (name, age, department) VALUES (%s, %s, %s);",
                (name, age, dept)
            )
        conn.commit()
        print(f"{n} record(s) inserted.")
        cursor.close()
    except Exception as e:
        print("Error inserting data:", e)

# Task 2: Update student department
def update_student(conn):
    try:
        cursor = conn.cursor()
        name = input("Enter student name to update: ")
        new_dept = input("Enter new department: ")
        cursor.execute("UPDATE Students SET department = %s WHERE name = %s;", (new_dept, name))
        conn.commit()
        print("Student department updated.")
        cursor.close()
    except Exception as e:
        print("Error updating data:", e)

# Task 2: Delete student
def delete_student(conn):
    try:
        cursor = conn.cursor()
        student_id = int(input("Enter student ID to delete: "))
        cursor.execute("DELETE FROM Students WHERE id = %s;", (student_id,))
        conn.commit()
        print("Student deleted.")
        cursor.close()
    except Exception as e:
        print("Error deleting data:", e)

# Task 3: Query operations
def query_data(conn):
    try:
        cursor = conn.cursor()
        print("\nQuery Options:")
        print("1. Display all students")
        print("2. Display by department")
        print("3. Average age by department")
        print("4. Students whose names start with a letter")
        choice = input("Enter choice: ")

        if choice == "1":
            cursor.execute("SELECT * FROM Students;")
        elif choice == "2":
            dept = input("Enter department: ")
            cursor.execute("SELECT * FROM Students WHERE department = %s;", (dept,))
        elif choice == "3":
            cursor.execute("SELECT department, AVG(age) FROM Students GROUP BY department;")
        elif choice == "4":
            letter = input("Enter starting letter: ")
            cursor.execute("SELECT * FROM Students WHERE name ILIKE %s;", (letter + "%",))
        else:
            print("Invalid choice.")
            return

        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()
    except Exception as e:
        print("Error querying data:", e)

# Menu-driven interaction
def menu():
    conn = connect_db()
    if not conn:
        return
    while True:
        print("\nMenu:")
        print("1. Create Table")
        print("2. Insert Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Query Data")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table(conn)
        elif choice == "2":
            insert_student(conn)
        elif choice == "3":
            update_student(conn)
        elif choice == "4":
            delete_student(conn)
        elif choice == "5":
            query_data(conn)
        elif choice == "6":
            conn.close()
            print("Goodbye.")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    menu()

