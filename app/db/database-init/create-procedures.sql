USE db_project;

-- Drop existing procedures
DROP PROCEDURE IF EXISTS GetGroupQuestionDetails;

DELIMITER //

-- Get detailed statistics for a specific group question
CREATE PROCEDURE GetGroupQuestionDetails(
    IN p_topic VARCHAR(100)
)
BEGIN
    WITH question_totals AS (
        SELECT 
            q.QID, 
            SUM(v.num_responses) as total_responses
        FROM v_question_summary v
        JOIN questions q ON v.QID = q.QID
        JOIN groupquestions g ON q.GID = g.GID
        WHERE g.GroupQuestion = p_topic
        GROUP BY q.QID
    )
    SELECT 
        q.qname as question_name,
        v.Answer,
        ROUND((v.num_responses * 100.0 / qt.total_responses), 2) as percentage
    FROM v_question_summary v
    JOIN questions q ON v.QID = q.QID
    JOIN groupquestions g ON q.GID = g.GID
    JOIN question_totals qt ON q.QID = qt.QID
    WHERE g.GroupQuestion = p_topic
    ORDER BY 
        q.qname,
        percentage DESC;
END //

DELIMITER ; 