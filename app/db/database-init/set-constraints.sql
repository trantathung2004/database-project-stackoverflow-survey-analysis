use db_project;

-- Question → GroupQuestion
ALTER TABLE questions
ADD CONSTRAINT fk_question_groupquestion
FOREIGN KEY (GID) REFERENCES group_questions(GID) ON DELETE CASCADE;

-- Question_Answer → Question
ALTER TABLE Question_Answer
ADD CONSTRAINT fk_qa_question
FOREIGN KEY (QID) REFERENCES questions(QID) ON DELETE CASCADE;

-- Question_Answer → Answer
ALTER TABLE Question_Answer
ADD CONSTRAINT fk_qa_answer
FOREIGN KEY (AnswerID) REFERENCES Answer(AnswerID) ON DELETE CASCADE;

-- Responses → Respondent
ALTER TABLE Responses
ADD CONSTRAINT fk_responses_respondent
FOREIGN KEY (ResponseID) REFERENCES Respondents(ResponseID) ON DELETE CASCADE;

-- Responses → Question
ALTER TABLE Responses
ADD CONSTRAINT fk_responses_question
FOREIGN KEY (QID) REFERENCES questions(QID) ON DELETE CASCADE;

-- Responses → Answer
ALTER TABLE Responses
ADD CONSTRAINT fk_responses_answer
FOREIGN KEY (AnswerID) REFERENCES answers(AnswerID) ON DELETE CASCADE;