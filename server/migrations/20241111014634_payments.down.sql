-- Add down migration script here
DROP TRIGGER IF EXISTS subscription_history_trigger;
DROP TRIGGER IF EXISTS new_subscription_history_trigger;
DROP TABLE IF EXISTS subscription_history;
DROP TABLE IF EXISTS subscription;
