--PART 1
--Q1
SELECT C.cname, F.fname
FROM Courses C
JOIN Faculty F ON C.instructor_fid = F.fid;
--Q2
SELECT S.sname FROM Students AS S 
INNER JOIN Enrolled AS E ON S.sid = E.sid
INNER JOIN Courses AS C ON C.cid = E.cid
INNER JOIN Faculty AS F ON C.instructor_fid = F.fid
WHERE F.fid = 1;

--Q3
SELECT S.sname, C.cname
FROM Students S
LEFT JOIN Enrolled E ON S.sid = E.sid
LEFT JOIN Courses C ON E.cid = C.cid;

--Q4
SELECT F.fname, C.cname
FROM Faculty F
LEFT JOIN Courses C ON F.fid = C.instructor_fid;


--PART2
--Q1
SELECT sname
FROM Students
WHERE LOWER(sname) LIKE '%a%';

--Q2
SELECT sid, sname
FROM Students
WHERE discip IS NULL;

--Q3
SELECT sname , registration_date FROM Students WHERE STRFTIME('%Y',registration_date) = '2022';

--Q4
SELECT sname FROM Students WHERE registration_date BETWEEN '2022-08-01' AND '2022-08-31';

--PART3
--Q1
SELECT sname
FROM Students
WHERE gpa > (SELECT AVG(gpa) FROM Students);

--Q2
SELECT s.sname from Students s where s.discip = 'CSE'
EXCEPT 
SELECT s.sname FROM Students s
JOIN Enrolled e ON s.sid = e.sid
WHERE e.cid = 'CSL303';

--Q3
SELECT c.cname from courses c
where EXISTS (
SELECT 1
FROM Enrolled e
WHERE c.cid = e.cid);

--Q4
SELECT S.sname, S.discip, S.gpa
FROM Students S
WHERE S.gpa = (
    SELECT MAX(S2.gpa)
    FROM Students S2
    WHERE S2.discip = S.discip
);

--PART4
--Q1
INSERT INTO Students (sid, sname, discip, gpa, registration_date)
VALUES (201, 'Ravi', 'EE', 8.0, '2023-09-01');

--Q2
UPDATE Students
SET gpa = MIN(gpa * 1.1, 10.0)
WHERE sid IN (
    SELECT E.sid
    FROM Enrolled E
    WHERE E.cid = 'CSL303' AND E.grade = 'A'
);

--Q3
DELETE FROM Enrolled
WHERE cid = 'MAL251';


