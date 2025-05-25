use db_project;

SET foreign_key_checks = 0;

drop table if exists questions;
CREATE TABLE Questions (
  QID INT PRIMARY KEY AUTO_INCREMENT,
  qname VARCHAR(100) NOT NULL,
  question TEXT NOT NULL,
  GID VARCHAR(100) NOT NULL,
  UNIQUE (GID, qname)
);

-- Table: Respondent
drop table if exists respondents;
CREATE TABLE Respondents (
ResponseID INT PRIMARY KEY AUTO_INCREMENT,
MainBranch VARCHAR(100),
Age VARCHAR(100),
Employment VARCHAR(100),
EdLevel VARCHAR(100),
Country VARCHAR(100)
);

-- Table: GroupQuestion
drop table if exists `GroupQuestions`;
CREATE TABLE `GroupQuestions` (
GID VARCHAR(100) PRIMARY KEY,
GroupQuestion VARCHAR(100) NOT NULL
);

drop table if exists answers;
CREATE TABLE Answers (
AnswerID INT PRIMARY KEY AUTO_INCREMENT,
Answer TEXT NOT NULL
);

-- Table: Question_Answer
drop table if exists Question_Answer;
CREATE TABLE Question_Answer (
QID INT,
AnswerID INT,
PRIMARY KEY (QID, AnswerID)
);

-- Table: Responses
drop table if exists Responses;
CREATE TABLE Responses (
ResponseID INT,
AnswerID INT,
QID INT,
PRIMARY KEY (ResponseID, AnswerID, QID)
);

drop table if exists Users
CREATE TABLE Users (
  
)