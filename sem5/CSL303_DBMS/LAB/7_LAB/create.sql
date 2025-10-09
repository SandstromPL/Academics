CREATE TABLE Students (
student_id INTEGER PRIMARY KEY,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
email TEXT NOT NULL UNIQUE,
major TEXT,
enrollment_date DATE
);
CREATE TABLE Courses (
course_id INTEGER PRIMARY KEY,
course_name TEXT NOT NULL,
department TEXT NOT NULL,
credits INTEGER
);
CREATE TABLE Enrollments (
enrollment_id INTEGER PRIMARY KEY,
student_id INTEGER,
course_id INTEGER,
grade REAL,
FOREIGN KEY(student_id) REFERENCES Students(student_id),
FOREIGN KEY(course_id) REFERENCES Courses(course_id)
);
