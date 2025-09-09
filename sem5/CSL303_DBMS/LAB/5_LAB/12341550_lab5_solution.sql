--PART 1
--1
select e.emp_name from Employees e
INNER JOIN Departments d ON e.dept_id = d.dept_id
where d.dept_name = "Marketing";

--2
SELECT emp_name , salary FROM Employees 
where salary > (SELECT avg(salary) from Employees);

--3
SELECT e.emp_name from Employees e
INNER JOIN Assignments a on a.emp_id = e.emp_id
INNER JOIN Projects p on p.proj_id = a.proj_id
where p.proj_name = "Project Phoenix";

--4
SELECT e.emp_name from Employees e
EXCEPT 
SELECT E.emp_name FROM Employees E
INNER JOIN Assignments A ON E.emp_id = A.emp_id;

--5
SELECT e.emp_name FROM Employees e
where e.salary > (
SELECT MIN(e2.salary) FROM Employees e2
INNER JOIN Departments d ON d.dept_id = e2.dept_id
WHERE d.dept_name = "Marketing"
);

--6
SELECT e.emp_name FROM Employees e
where e.salary > (
SELECT MAX(e2.salary) FROM Employees e2
INNER JOIN Departments d ON d.dept_id = e2.dept_id
WHERE d.dept_name = "Marketing"
);

--PART2
--1
SELECT emp_name FROM Employees WHERE STRFTIME('%Y', hire_date ) = '2023';

--2
SELECT emp_name FROM Employees WHERE manager_id IS NULL;

--3
SELECT emp_name FROM Employees WHERE emp_name LIKE '%Smith' OR emp_name LIKE '%Williams';

--4
SELECT emp_name FROM Employees
WHERE hire_date >= DATE('now', '-2 years');

--PART 3
--1
SELECT d.dept_name, e.emp_name, e.salary
FROM Employees e
INNER JOIN Departments d ON e.dept_id = d.dept_id
INNER JOIN (
    SELECT dept_id, MAX(salary) AS max_salary
    FROM Employees
    GROUP BY dept_id
) AS max_salaries ON e.dept_id = max_salaries.dept_id AND e.salary = max_salaries.max_salary;

--2
SELECT e.emp_name FROM Employees e
   ...> INNER JOIN Departments d ON d.dept_id = e.dept_id
   ...> WHERE d.dept_name = "Engineering"
   ...> EXCEPT 
   ...> SELECT e2.emp_name FROM Employees e2
   ...> INNER JOIN Assignments a ON a.emp_id = e2.emp_id
   ...> INNER JOIN Projects p ON p.proj_id = a.proj_id
   ...> WHERE p.proj_name = "Project Neptune";

--3
SELECT d.dept_name
FROM Employees e
INNER JOIN Departments d ON e.dept_id = d.dept_id
GROUP BY d.dept_name
HAVING AVG(e.salary) > (
    SELECT AVG(salary)
    FROM Employees
);

--PART4
--1
ALTER TABLE Employees
ADD COLUMN email TEXT;

--2
UPDATE Employees
SET email = LOWER(REPLACE(emp_name, ' ', '')) || '@engineering.com'
WHERE dept_id = (
    SELECT dept_id
    FROM Departments
    WHERE dept_name = 'Engineering'
);

--3
CREATE TABLE HighEarners (
    emp_id INTEGER,
    emp_name TEXT
);

INSERT INTO HighEarners (emp_id, emp_name)
SELECT emp_id, emp_name
FROM Employees
WHERE salary > 95000;
