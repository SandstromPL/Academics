--PART1
--1
select sname,Gpa from students where discipline=="Physics";

--2
select cid,credits from courses where credits==4;


--3
select sid,cid from enrolled where grade=="F";


--4
select discipline,sname from students order by discipline,sname;


--PART 2

--1
SELECT students.sname  FROM students INNER JOIN enrolled ON students.sid = enrolled.sid where enrolled.cid="CSL303";

--2
SELECT courses.cname
FROM enrolled
INNER JOIN students ON students.sid = enrolled.sid
INNER JOIN courses ON courses.cid = enrolled.cid
WHERE students.sname = 'Ben Taylor';

-- 3
SELECT DISTINCT students.sname,courses.cname,enrolled.grade
FROM enrolled
INNER JOIN students ON students.sid = enrolled.sid
INNER JOIN courses ON courses.cid = enrolled.cid Order by students.sname,courses.cname;


--4

select sname from students where sid not in (select sid from enrolled);

-- 5
SELECT students.sname                           
FROM enrolled 
INNER JOIN students ON students.sid = enrolled.sid
INNER JOIN courses ON courses.cid = enrolled.cid where enrolled.grade="B"AND courses.credits=3;



--PART 3

--1

select discipline,count(sname) as [no. of students]  from students group by discipline;

--2
select credits,count(cid) as [no. of courses]  from courses group by credits;


--3
select courses.cname,count(*)  from courses INNER JOIN enrolled on courses.cid=enrolled.cid group by  enrolled.cid;


--4
select cid from enrolled where grade="A" group by cid having count(sid) >2;

