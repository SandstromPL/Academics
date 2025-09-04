/*
CREATING TABLE
sqlite> create table Students (
(x1...> StudentID integer primary key,
(x1...> FirstName text not null,
(x1...> LastName text not null,
(x1...> Discipline text
(x1...> );
sqlite> create table Faculty (
(x1...> FacultyID integer primary key,
(x1...> FirstName text not null,
(x1...> LastName text not null,
(x1...> Department text);

*/

/*
INSERTING INTO TABLE
sqlite> INSERT INTO Students (StudentID, FirstName, LastName, Discipline)
   ...> VALUES 
   ...> (101,'Rahul','Sharma','CSE'),
   ...> (102,'Priya','Verma','Mechanical'),
   ...> (103,'Ankit','Patel','Electrical'),
   ...> (104,'Sneha','Mehta','Civil'),
   ...> (105,'Amit','Reddy','Chemical');
sqlite> .tables
Faculty   Students
sqlite> INSERT INTO Faculty (FacultyID, FirstName, LastName, Department)
   ...> VALUES
   ...> (201,'Rahul','Reddy','CSE'),
   ...> (202,'Sneha','Kapoor','Electrical'),
   ...> (203,'Anjali','Mehta','Civil'),
   ...> (204,'Amit','Sharma','Mechanical'),
   ...> (205,'Karan','Patel','Chemical');

*/


/*
Task
1. Find all students with discipline ’CSE’.
2. Find all faculty in the ’CSE’ department.
*/
SELECT * FROM Students WHERE Discipline = 'CSE';
SELECT * FROM Faculty WHERE Department = 'CSE';

/*
Task
1. List the first and last names of all students.
2. List the last names and departments of all faculty.
*/
SELECT FirstName , LastName FROM Students;
SELECT LastName ,Department FROM Faculty;

/*
Task
1. List all unique first names of both students and faculty.
2. List all unique last names of both students and faculty.
*/
SELECT FirstName FROM Students UNION SELECT FirstName FROM Faculty;
SELECT LastName FROM Students UNION SELECT LastName FROM Faculty;

/*
Task
1. Find all first names that are common to both students and faculty.
2. Find all last names that are common to both students and faculty.
*/
SELECT FirstName FROM Students INTERSECT SELECT FirstName FROM Faculty;
SELECT LastName FROM Students INTERSECT SELECT LastName FROM Faculty;
