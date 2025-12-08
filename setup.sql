
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
name            VARCHAR(80),
dept			VARCHAR(50),
office			VARCHAR(50),
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
prof_id			INT PRIMARY KEY,
name            VARCHAR(80),
dept 			VARCHAR(50),
office			VARCHAR(50),
start_date		VARCHAR(50),
password		VARCHAR(50)
);

CREATE TABLE Class (
course_id	INT PRIMARY KEY,
title 		VARCHAR(50),
prof_id		INT,
FOREIGN KEY(prof_id) REFERENCES Professor(prof_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);

CREATE TABLE Is_in (
student_id		INT,
course_id		INT,
grade 		    INT,
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
stu_id          INT,
title			VARCHAR(50),
point_value		INT,
grade			INT,
description		VARCHAR(80),
due_date		VARCHAR(50),
completed 		BOOLEAN,
PRIMARY KEY (course_id, title),
FOREIGN KEY (course_id) REFERENCES Class(course_id)
FOREIGN KEY (stu_id) REFERENCES Student(student_id)
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

INSERT INTO Advisor Values(1041, "Dobby Theelf", 
"Comp Sci", "Comp Sci 205", "10/12/24", "AdVis0rsRUl3");

INSERT INTO Student VALUES(1203, "Freddie Mercury", 
false, 1041, "basedstudent123");

INSERT INTO Professor VALUES(1544, "Homer Simpson", 
"Comp sci", "Comp Sci 302", "9/23/21", "B3stT3acher");

INSERT INTO Assignment VALUES(4150, 1203, "AI Research Project", 30, 0, "Evolution of Artificial Intelligence", "2025-12-10", false);

INSERT INTO Assignment VALUES(4150, 1203, "Quiz 1", 20, 0, "Machine Learning Basics", "2025-12-12", false);

INSERT INTO Assignment VALUES(4200, 1203, "Exam 1", 50, 0, "Linked Lists and Trees", "2025-12-15", false);

INSERT INTO Class VALUES(4150, "Intro to AI", 1544);

INSERT INTO Class VALUES(4200, "Data Structures", 1544);

INSERT INTO Is_in VALUES(1203, 4150, 88);

INSERT INTO Is_in VALUES(1203, 4200, 92);

INSERT INTO Exam VALUES(4150, "Exam 1", "CS101");

INSERT INTO Quiz VALUES(4150, "Quiz 1", 45);

INSERT INTO Project VALUES(4150, "AI Research Project", 3);

Select * From Advisor;
Select * From Student;
select * from Class;
select * from Professor;
select * from Is_in;
select * from Assignment;