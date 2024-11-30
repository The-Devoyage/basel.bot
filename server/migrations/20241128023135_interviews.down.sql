-- Add down migration script here
DROP TRIGGER IF EXISTS interview_history_trigger;
DROP TRIGGER IF EXISTS new_interview_history_trigger;
DROP TABLE IF EXISTS interview_history;
DROP TABLE IF EXISTS interview;

DROP TRIGGER IF EXISTS interview_question_history_trigger;
DROP TRIGGER IF EXISTS new_interiew_question_history_trigger;
DROP TABLE IF EXISTS interview_question_history;
DROP TABLE IF EXISTS interview_question;

DROP TRIGGER IF EXISTS interview_question_response_history_trigger;
DROP TRIGGER IF EXISTS new_interiew_question_response_history_trigger;
DROP TABLE IF EXISTS interview_question_response_history;
DROP TABLE IF EXISTS interview_question_response;
