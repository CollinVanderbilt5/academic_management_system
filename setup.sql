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

INSERT INTO Advisor Values(1, "White House", "Comp Scie", "10/12/24", "I love Obama");
INSERT INTO Student VALUES(1,"Dorian",false,1, "Marikiplier");

Select * From Advisor;
Select * From Student;