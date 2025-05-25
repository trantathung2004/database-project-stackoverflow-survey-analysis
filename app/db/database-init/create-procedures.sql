USE db_project;

DROP PROCEDURE IF EXISTS GetQuestionStatsByAgeGroup;

DELIMITER //

CREATE PROCEDURE GetQuestionStatsByAgeGroup(
    IN p_question_id INT
)
BEGIN
    -- Get statistics for each age group
    SELECT 
        resp.Age as age_group,
        q.qname as question,
        a.Answer,
        COUNT(r.ResponseID) as response_count,
        ROUND(COUNT(r.ResponseID) * 100.0 / (
            SELECT COUNT(*) 
            FROM Responses r2 
            JOIN Respondents resp2 ON r2.ResponseID = resp2.ResponseID
            WHERE r2.QID = p_question_id
            AND resp2.Age = resp.Age
        ), 2) as percentage
    FROM Questions q
    JOIN Responses r ON r.QID = q.QID
    JOIN Respondents resp ON r.ResponseID = resp.ResponseID
    JOIN Answers a ON r.AnswerID = a.AnswerID
    WHERE q.QID = p_question_id
    GROUP BY resp.Age, q.qname, a.Answer
    ORDER BY 
        CASE resp.Age
            WHEN 'Under 18 years old' THEN 1
            WHEN '18-24 years old' THEN 2
            WHEN '25-34 years old' THEN 3
            WHEN '35-44 years old' THEN 4
            WHEN '45-54 years old' THEN 5
            WHEN '55-64 years old' THEN 6
            WHEN '65 years or older' THEN 7
            ELSE 8
        END,
        response_count DESC;
END //

DELIMITER ; 

DELIMITER $$

CREATE PROCEDURE InsertRespondentWithResponse (
    IN p_MainBranch VARCHAR(100),
    IN p_Age VARCHAR(100),
    IN p_Country VARCHAR(100),
    IN p_Employment VARCHAR(100),
    IN p_EdLevel VARCHAR(100),
    IN p_AnswerID INT,
    IN p_QID INT
)
BEGIN
    DECLARE last_id INT;

    -- Insert into Respondents
    INSERT INTO Respondents (MainBranch, Age, Country, Employment, EdLevel)
    VALUES (p_MainBranch, p_Age, p_Country, p_Employment, p_EdLevel);

    -- Get the inserted ResponseID (primary key)
    SET last_id = LAST_INSERT_ID();

    -- Insert into Responses
    INSERT INTO Responses (ResponseID, AnswerID, QID)
    VALUES (last_id, p_AnswerID, p_QID);
END$$

DELIMITER ;
