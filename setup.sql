
DROP TABLE IF EXISTS Assignment;
DROP TABLE IF EXISTS Exam;
DROP TABLE IF EXISTS Quiz;
DROP TABLE IF EXISTS Project;
DROP TABLE IF EXISTS Is_in;
DROP TABLE IF EXISTS Class;
DROP TABLE IF EXISTS Professor;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Advisor;

CREATE TABLE Advisor (
advisor_id 		INT PRIMARY KEY,
office			VARCHAR(50),
dept			VARCHAR(50),
start_date		VARCHAR(50),
password		VARCHAR(50)
);

CREATE TABLE Student (
student_id		INT PRIMARY KEY,
name			VARCHAR(80),
advising_hold		BOOLEAN,
advisor_id		INT,
password		VARCHAR(50),
FOREIGN KEY (advisor_id) REFERENCES Advisor(advisor_id)
ON DELETE SET NULL
ON UPDATE CASCADE
);

CREATE TABLE Professor (
prof_id			 INT PRIMARY KEY,
dept 			VARCHAR(50),
office			VARCHAR(50),
start_date		VARCHAR(50),
password		VARCHAR(50)
);

CREATE TABLE Class (
course_id	INT PRIMARY KEY,
grade 		INT,
title 		VARCHAR(50),
prof_id		INT,
FOREIGN KEY(prof_id) REFERENCES Professor(prof_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE Is_in (
student_id		INT,
course_id		INT,
PRIMARY KEY (student_id, course_id),
FOREIGN KEY (student_id) REFERENCES Student(student_id)
ON DELETE CASCADE
ON UPDATE CASCADE,
FOREIGN KEY (course_id) REFERENCES Class(course_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE Assignment (
course_id 		INT,
title			VARCHAR(50),
point_value		INT,
grade			INT,
description		VARCHAR(80),
due_date		VARCHAR(50),
completed 		BOOLEAN,
PRIMARY KEY (course_id, title),
FOREIGN KEY (course_id) REFERENCES Class(course_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE Exam (
course_id 	INT,
title		Char(40),
room		Char(40),
PRIMARY KEY (course_id,title,room),
FOREIGN KEY (course_id) REFERENCES Class(course_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE Quiz (
course_id 	INT,
title		Char(40),
duration	INT,
PRIMARY KEY (course_id,title,duration),
FOREIGN KEY(course_id) REFERENCES Class(course_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE Project (
course_id 	INT,
title		Char(20),
partners	INT,
PRIMARY KEY (course_id, title, partners),
FOREIGN KEY (course_id) REFERENCES Class(course_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);


INSERT INTO Advisor Values(1, "White House", "Comp Scie", "10/12/24", "I love Obama");
INSERT INTO Student VALUES(1,"Dorian",false,1, "Marikiplier");

Select * From Advisor;
Select * From Student;
select * from Class;
select * from Professor;
select * from Is_in;