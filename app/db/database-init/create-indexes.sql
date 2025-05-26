use db_project;

CREATE INDEX idx_respondent_uid ON Respondents(ResponseID);

CREATE INDEX idx_question_gid ON Questions(GID);
CREATE INDEX idx_question_qname ON Questions(qname);

CREATE FULLTEXT INDEX ft_answer_text ON Answers(Answer);

CREATE INDEX idx_responses_responseid ON Responses(ResponseID);
CREATE INDEX idx_responses_qid ON Responses(QID);
CREATE INDEX idx_responses_answerid ON Responses(AnswerID);
