Lab 8: Programming Language with DBMS
Name: Paritosh Lahre
Roll No.: 12341550

Overview:
This lab demonstrates how to integrate a programming language (Python) with a PostgreSQL database running inside a Docker container.
The program performs all basic database operations such as DDL, DML, and queries through a simple text-based menu interface.

Requirements:
    1. Docker
    2. Python 3.12
    3. pip

Instructions:
    1. Run the given commands (after running Docker):
        docker pull postgres
        docker run --name pg_lab -e POSTGRES_PASSWORD=admin123 -p 5432:5432 -d postgres

    2. Check that the container is running:
        docker ps

    3. Access the container shell:
        docker exec -it pg_lab psql -U postgres

    4. Create database:
        CREATE DATABASE studentdb;
        \q

    5. Install dependencies (preferably inside a virtual environment):
        pip install -r requirements.txt

    6. Run the script from your terminal:
        python lab8.py

Features:
    1. Create Table: Builds the Students table inside studentdb.

    2. Insert Student: Adds new records through user input.

    3. Update Student: Updates a student’s department by name.

    4. Delete Student: Deletes a student by ID.

    5. Query Data:

        a. View all students

        b. Filter by department

        c. Show average age per department

        d. Search by name prefix

    6. Exit: Closes the database connection gracefully.

To cleanup:

    1. To stop and remove the database container:
        docker stop pg_lab
        docker rm pg_lab





