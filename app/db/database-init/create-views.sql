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

drop view if exists v_history_response;
CREATE VIEW v_history_response AS
SELECT
r.ResponseID,
r.MainBranch,
r.Age,
r.Employment,
r.Country,
r.EdLevel,
r.UID,
GROUP_CONCAT(CASE WHEN q.qname = 'LanguageHaveWorkedWith' THEN a.Answer END SEPARATOR ';') AS LanguageHaveWorkedWith,
GROUP_CONCAT(CASE WHEN q.qname = 'LanguageWantToWorkWith' THEN a.Answer END SEPARATOR ';') AS LanguageWantToWorkWith,
GROUP_CONCAT(CASE WHEN q.qname = 'DatabaseHaveWorkedWith' THEN a.Answer END SEPARATOR ';') AS DatabaseHaveWorkedWith,
GROUP_CONCAT(CASE WHEN q.qname = 'DatabaseWantToWorkWith' THEN a.Answer END SEPARATOR ';') AS DatabaseWantToWorkWith,
GROUP_CONCAT(CASE WHEN q.qname = 'WebframeHaveWorkedWith' THEN a.Answer END SEPARATOR ';') AS WebframeHaveWorkedWith,
GROUP_CONCAT(CASE WHEN q.qname = 'WebframeWantToWorkWith' THEN a.Answer END SEPARATOR ';') AS WebframeWantToWorkWith,
GROUP_CONCAT(CASE WHEN q.qname = 'LearnCode' THEN a.Answer END SEPARATOR ';') AS LearnCode,
GROUP_CONCAT(CASE WHEN q.qname = 'LearnCodeOnline' THEN a.Answer END SEPARATOR ';') AS LearnCodeOnline,
GROUP_CONCAT(CASE WHEN q.qname = 'AISelect' THEN a.Answer END SEPARATOR ';') AS AISelect,
GROUP_CONCAT(CASE WHEN q.qname = 'AIThreat' THEN a.Answer END SEPARATOR ';') AS AIThreat,
GROUP_CONCAT(CASE WHEN q.qname = 'AIToolCurrentlyUsing' THEN a.Answer END SEPARATOR ';') AS AIToolCurrentlyUsing,
GROUP_CONCAT(CASE WHEN q.qname = 'OpSysPersonalUse' THEN a.Answer END SEPARATOR ';') AS OpSysPersonalUse,
GROUP_CONCAT(CASE WHEN q.qname = 'OpSysProfessionalUse' THEN a.Answer END SEPARATOR ';') AS OpSysProfessionalUse
FROM Respondents r
LEFT JOIN Responses rs ON r.ResponseID = rs.ResponseID
LEFT JOIN Answers a ON a.AnswerID = rs.AnswerID
LEFT JOIN Questions q ON q.QID = rs.QID
GROUP BY r.ResponseID;


# Respondents' Demographic
CREATE VIEW v_respondent_summary AS
SELECT
	Country,
	Employment,
	EdLevel,
	COUNT(*) AS total_respondents
FROM Respondents
GROUP BY Country, Employment, EdLevel;


