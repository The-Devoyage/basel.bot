-- Add up migration script here
CREATE TABLE subscription(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  user_id INTEGER NOT NULL,
  customer_id TEXT DEFAULT NULL,
  checkout_session_id TEXT NOT NULL,
  status BOOLEAN NOT NULL DEFAULT 0,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE subscription_history(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subscription_id INTEGER,
  uuid TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  customer_id TEXT DEFAULT NULL,
  checkout_session_id TEXT NOT NULL,
  status BOOLEAN NOT NULL DEFAULT 0,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_subscription_history_trigger
AFTER INSERT ON subscription
BEGIN
  INSERT INTO subscription_history (subscription_id, uuid, user_id, customer_id, checkout_session_id, status, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.user_id, NEW.customer_id, NEW.checkout_session_id, NEW.status, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER subscription_history_trigger
AFTER UPDATE ON subscription 
BEGIN
  INSERT INTO subscription_history (subscription_id, uuid, user_id, customer_id, checkout_session_id, status, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.user_id, NEW.customer_id, NEW.checkout_session_id, NEW.status, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

