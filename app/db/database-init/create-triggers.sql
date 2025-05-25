USE db_project;

-- Create audit log table
CREATE TABLE IF NOT EXISTS response_audit_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    response_id INT,
    question_id INT,
    answer_id INT,
    action_type ENUM('INSERT', 'UPDATE', 'DELETE'),
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_value TEXT,
    new_value TEXT
);

DELIMITER //

-- Trigger for INSERT
CREATE TRIGGER after_response_insert
AFTER INSERT ON Responses
FOR EACH ROW
BEGIN
    INSERT INTO response_audit_log (
        response_id, 
        question_id, 
        answer_id, 
        action_type,
        new_value
    ) VALUES (
        NEW.ResponseID,
        NEW.QID,
        NEW.AnswerID,
        'INSERT',
        (SELECT Answer FROM Answers WHERE AnswerID = NEW.AnswerID)
    );
END//

-- Trigger for UPDATE
CREATE TRIGGER after_response_update
AFTER UPDATE ON Responses
FOR EACH ROW
BEGIN
    INSERT INTO response_audit_log (
        response_id, 
        question_id, 
        answer_id, 
        action_type,
        old_value,
        new_value
    ) VALUES (
        NEW.ResponseID,
        NEW.QID,
        NEW.AnswerID,
        'UPDATE',
        (SELECT Answer FROM Answers WHERE AnswerID = OLD.AnswerID),
        (SELECT Answer FROM Answers WHERE AnswerID = NEW.AnswerID)
    );
END//

-- Trigger for DELETE
CREATE TRIGGER after_response_delete
AFTER DELETE ON Responses
FOR EACH ROW
BEGIN
    INSERT INTO response_audit_log (
        response_id, 
        question_id, 
        answer_id, 
        action_type,
        old_value
    ) VALUES (
        OLD.ResponseID,
        OLD.QID,
        OLD.AnswerID,
        'DELETE',
        (SELECT Answer FROM Answers WHERE AnswerID = OLD.AnswerID)
    );
END//

DELIMITER ; 