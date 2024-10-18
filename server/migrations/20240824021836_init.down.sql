-- Add down migration script here

-- Drop Entities
DROP TRIGGER IF EXISTS message_history_trigger;
DROP TRIGGER IF EXISTS new_message_history_trigger;
DROP TABLE IF EXISTS message_history;
DROP TABLE IF EXISTS message;

DROP TRIGGER IF EXISTS user_history_trigger;
DROP TRIGGER IF EXISTS new_user_history_trigger;
DROP TABLE IF EXISTS user_history;
DROP TABLE IF EXISTS user;

DROP TRIGGER IF EXISTS user_profile_history_trigger;
DROP TRIGGER IF EXISTS new_user_profile_history_trigger;
DROP TABLE IF EXISTS user_profile_history;
DROP TABLE IF EXISTS user_profile;

DROP TRIGGER IF EXISTS organization_history_trigger;
DROP TRIGGER IF EXISTS new_organization_history_trigger;
DROP TABLE IF EXISTS organization_history;
DROP TABLE IF EXISTS organization;

DROP TRIGGER IF EXISTS file_history_trigger;
DROP TRIGGER IF EXISTS new_file_history_trigger;
DROP TABLE IF EXISTS file_history;
DROP TABLE IF EXISTS file;

DROP TRIGGER IF EXISTS posting_history_trigger;
DROP TRIGGER IF EXISTS new_posting_history_trigger;
DROP TABLE IF EXISTS posting_history;
DROP TABLE IF EXISTS posting;

DROP TRIGGER IF EXISTS application_history_trigger;
DROP TRIGGER IF EXISTS new_application_history_trigger;
DROP TABLE IF EXISTS application_history;
DROP TABLE IF EXISTS application;

DROP TRIGGER IF EXISTS posting_skill_history_trigger;
DROP TRIGGER IF EXISTS new_posting_skill_history_trigger;
DROP TABLE IF EXISTS posting_skill_history;
DROP TABLE IF EXISTS posting_skill;

DROP TRIGGER IF EXISTS user_profile_skill_history_trigger;
DROP TRIGGER IF EXISTS new_user_profile_skill_history_trigger;
DROP TABLE IF EXISTS user_profile_skill_history;
DROP TABLE IF EXISTS user_profile_skill;

DROP TRIGGER IF EXISTS user_profile_education_history_trigger;
DROP TRIGGER IF EXISTS new_user_profile_education_history_trigger;
DROP TABLE IF EXISTS user_profile_education_history;
DROP TABLE IF EXISTS user_profile_education;

DROP TRIGGER IF EXISTS organization_user_history_trigger;
DROP TRIGGER IF EXISTS new_organization_user_history_trigger;
DROP TABLE IF EXISTS organization_user_history;
DROP TABLE IF EXISTS organization_user;

-- Drop References Tables
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS application_status;
DROP TABLE IF EXISTS skill;

