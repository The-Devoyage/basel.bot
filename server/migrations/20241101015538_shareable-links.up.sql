-- Add up migration script here

CREATE TABLE shareable_link (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  tag TEXT DEFAULT NULL,
  token TEXT DEFAULT NULL,
  status BOOLEAN DEFAULT true,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE shareable_link_history(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  shareable_link_id INTEGER NOT NULL,
  uuid TEXT NOT NULL,
  tag TEXT DEFAULT NULL,
  token TEXT DEFAULT NULL,
  status BOOLEAN DEFAULT true,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_shareable_link_history_trigger
AFTER INSERT ON shareable_link 
BEGIN
  INSERT INTO shareable_link_history(shareable_link_id, uuid, tag, token, status, created_by, updated_by, deleted_by, created_at, updated_at, deleted_at)
  SELECT NEW.id, NEW.uuid, NEW.tag, NEW.token, NEW.status, NEW.created_by, NEW.updated_by, NEW.deleted_by, NEW.created_at, NEW.updated_at, NEW.deleted_at;
END;
CREATE TRIGGER shareable_link_history_trigger
AFTER UPDATE ON shareable_link 
BEGIN
  INSERT INTO shareable_link_history (shareable_link_id, uuid, tag, token, status, created_by, updated_by, deleted_by, created_at, updated_at, deleted_at)
  SELECT NEW.id, NEW.uuid, NEW.tag, NEW.token, NEW.status, NEW.created_by, NEW.updated_by, NEW.deleted_by, NEW.created_at, NEW.updated_at, NEW.deleted_at;
END;
