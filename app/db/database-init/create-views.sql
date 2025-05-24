use db_project;

# Overall Question Result Summary
CREATE VIEW v_question_summary AS
SELECT
	q.QID,
	q.qname,
	q.question,
	a.Answer,
COUNT(r.ResponseID) AS num_responses
FROM Responses r
JOIN Questions q ON r.QID = q.QID
JOIN Answers a ON r.AnswerID = a.AnswerID
GROUP BY q.QID, a.AnswerID;

# Respondents' Demographic
CREATE VIEW v_respondent_summary AS
SELECT
	Country,
	Employment,
	EdLevel,
	COUNT(*) AS total_respondents
FROM Respondents
GROUP BY Country, Employment, EdLevel;

