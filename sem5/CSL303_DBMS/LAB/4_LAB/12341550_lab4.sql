--Q1
CREATE TABLE enrolled( student_id integer PRIMARY KEY , course_id Integer,);

--Q2
INSERT INTO enrolled (student_id , course_id ) SELECT student_id , course_id FROM Enrollments ;

--Q3
UPDATE Students  SET department = 'Philosophy' WHERE name LIKE '%i%';

--Q4
ALTER TABLE Students  ADD COLUMN email TEXT;

--Q5
UPDATE Students  SET email = lower(name) || 'iitbhilai.ac.in';

--Q6
SELECT name FROM  Students where department = 'Computer Science';

--Q7
SELECT name FROM Students  where student_id in( select student_id FROM enrolled);

--Q8
SELECT s.name , c.course_name  FROM Students s INNER JOIN enrolled e ON e.student_id = s.student_id INNER JOIN Courses c ON c.course_id = e.course_id ORDER BY c.course_name;

--Q9
SELECT s.name , c.course_name FROM Students s LEFT OUTER JOIN enrolled e ON e.student_id = s.student_id LEFT OUTER JOIN Courses c ON c.course_id = e.course_id;

--Q10
SELECT name FROM Students WHERE name LIKE 'A%';

--Q11
SELECT s.name FROM Students s INNER JOIN enrolled e ON e.student_id = s.student_id INNER JOIN Courses c ON c.course_id = e.course_id WHERE c.credits > 3;

--Q12
SELECT name FROM Students EXCEPT  SELECT s.name FROM Students s INNER JOIN enrolled e ON e.student_id = s.student_id;

