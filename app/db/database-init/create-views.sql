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

CREATE VIEW v_history_response AS
SELECT
r.ResponseID,
r.MainBranch,
r.Age,
r.Employment,
r.Country,
r.EdLevel,
GROUP_CONCAT(CASE WHEN q.qname = 'LanguageWorkedWith' THEN a.Answer END SEPARATOR ';') AS LanguageWorkedWith,
GROUP_CONCAT(CASE WHEN q.qname = 'LanguageWantToWorkWith' THEN a.Answer END SEPARATOR ';') AS LanguageWantToWorkWith,
GROUP_CONCAT(CASE WHEN q.qname = 'AISelect' THEN a.Answer END SEPARATOR ';') AS AISelect,
GROUP_CONCAT(CASE WHEN q.qname = 'LearnCode' THEN a.Answer END SEPARATOR ';') AS LearnCode,
GROUP_CONCAT(CASE WHEN q.qname = 'LearningSources' THEN a.Answer END SEPARATOR ';') AS LearningSources,
GROUP_CONCAT(CASE WHEN q.qname = 'Motivation' THEN a.Answer END SEPARATOR ';') AS Motivation,
GROUP_CONCAT(CASE WHEN q.qname = 'OpSysProfessional use' THEN a.Answer END SEPARATOR ';') AS 'OpSysProfessional use'
-- Add more CASEs for other qname values if needed
FROM Respondents r
LEFT JOIN Responses rs ON r.ResponseID = rs.ResponseID
LEFT JOIN Answers a ON a.AnswerID = rs.AnswerID
LEFT JOIN Questions q ON q.QID = rs.QID
GROUP BY r.ResponseID
LIMIT 100;


# Respondents' Demographic
CREATE VIEW v_respondent_summary AS
SELECT
	Country,
	Employment,
	EdLevel,
	COUNT(*) AS total_respondents
FROM Respondents
GROUP BY Country, Employment, EdLevel;


