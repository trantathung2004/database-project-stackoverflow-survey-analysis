create database db_project;
SET foreign_key_checks = 0;

drop table if exists question;
CREATE TABLE Question (
  QID INT PRIMARY KEY AUTO_INCREMENT,
  qname VARCHAR(100) NOT NULL,
  question TEXT NOT NULL,
  GID VARCHAR(100) NOT NULL,
  UNIQUE (GID, qname)
);

-- Table: Respondent
drop table if exists respondent;
CREATE TABLE Respondent (
ResponseID INT PRIMARY KEY AUTO_INCREMENT,
MainBranch VARCHAR(100),
Age VARCHAR(100),
Country VARCHAR(100),
Employment VARCHAR(100),
EdLevel VARCHAR(100)
);

-- Table: GroupQuestion
drop table if exists groupquestion;
CREATE TABLE `Group` (
GID VARCHAR(100) PRIMARY KEY,
GroupQuestionName VARCHAR(100) NOT NULL
);

CREATE TABLE Answer (
AnswerID INT PRIMARY KEY AUTO_INCREMENT,
AnswerText TEXT NOT NULL
);

-- Table: Question_Answer
CREATE TABLE Question_Answer (
QID INT,
AnswerID INT,
PRIMARY KEY (QID, AnswerID)
);

-- Table: Responses
CREATE TABLE Responses (
ResponseID INT,
QID INT,
AnswerID INT,
qname VARCHAR(100),
PRIMARY KEY (ResponseID, QID)
);