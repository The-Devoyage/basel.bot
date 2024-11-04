-- Add down migration script here
DROP TRIGGER IF EXISTS shareable_link_history;
DROP TRIGGER IF EXISTS new_shareable_link_history;
DROP TABLE IF EXISTS shareable_link_history;
DROP TABLE IF EXISTS shareable_link;
