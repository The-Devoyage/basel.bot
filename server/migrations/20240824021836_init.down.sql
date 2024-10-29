-- Add down migration script here

-- Drop Entities
DROP TRIGGER IF EXISTS message_history_trigger;
DROP TRIGGER IF EXISTS new_message_history_trigger;
DROP TABLE IF EXISTS message_history;
DROP TABLE IF EXISTS message;

-- Drop Token Session
DROP TABLE IF EXISTS token_session;

DROP TRIGGER IF EXISTS user_history_trigger;
DROP TRIGGER IF EXISTS new_user_history_trigger;
DROP TABLE IF EXISTS user_history;
DROP TABLE IF EXISTS user;

DROP TRIGGER IF EXISTS user_meta_history_trigger;
DROP TRIGGER IF EXISTS new_user_meta_history_trigger;
DROP TABLE IF EXISTS user_meta_history;
DROP TABLE IF EXISTS user_meta;

DROP TRIGGER IF EXISTS file_history_trigger;
DROP TRIGGER IF EXISTS new_file_history_trigger;
DROP TABLE IF EXISTS file_history;
DROP TABLE IF EXISTS file;

-- Drop References Tables
DROP TABLE IF EXISTS role;

