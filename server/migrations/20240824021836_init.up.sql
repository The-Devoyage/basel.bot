-- Init the DB for a Job Posting Website - sqlite3

-- ENTITY TABLES
----------------------------------------------

-- Create Table user 
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  first_name TEXT DEFAULT NULL,
  last_name TEXT DEFAULT NULL,
  phone TEXT UNIQUE,
  role_id INTEGER NOT NULL, 
  status BOOLEAN NOT NULL DEFAULT 0,
  profile_image INTEGER,
  auth_id TEXT NOT NULL,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (profile_image) REFERENCES file(id),
  FOREIGN KEY (role_id) REFERENCES role(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE user_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  email TEXT NOT NULL,
  first_name TEXT DEFAULT NULL,
  last_name TEXT DEFAULT NULL,
  phone TEXT,
  role_id INTEGER NOT NULL, 
  status BOOLEAN NOT NULL DEFAULT 0,
  profile_image INTEGER,
  auth_id TEXT NOT NULL,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (profile_image) REFERENCES file(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (role_id) REFERENCES role(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_user_history_trigger
AFTER INSERT ON user
BEGIN
  INSERT INTO user_history (user_id, uuid, email, first_name, last_name, phone, role_id, status, profile_image, auth_id, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.email, NEW.first_name, NEW.last_name, NEW.phone, NEW.role_id, NEW.status, NEW.profile_image, NEW.auth_id, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER user_history_trigger
AFTER UPDATE ON user
BEGIN
  INSERT INTO user_history (user_id, uuid, email, first_name, last_name, phone, role_id, status, profile_image, auth_id, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.email, NEW.first_name, NEW.last_name, NEW.phone, NEW.role_id, NEW.status, NEW.profile_image, NEW.auth_id, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

-- Create Table message
CREATE TABLE message (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  user_id INTEGER NOT NULL,
  sender TEXT NOT NULL CHECK (sender IN ('user', 'bot')),
  text TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
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
CREATE TABLE message_history(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  message_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  sender TEXT NOT NULL CHECK (sender IN ('user', 'bot')),
  text TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (message_id) REFERENCES message(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_message_history_trigger
AFTER INSERT ON message
BEGIN
  INSERT INTO message_history (message_id, uuid, user_id, sender, text, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.user_id, NEW.sender, NEW.text, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER message_history_trigger
AFTER UPDATE ON message
BEGIN
  INSERT INTO message_history (message_id, uuid, user_id, sender, text, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.user_id, NEW.sender, NEW.text, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

-- Create Table User Meta
-- The AI extracts datapoints from the conversation/messages and stores them here
CREATE TABLE user_meta (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  data TEXT NOT NULL,
  tags TEXT DEFAULT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
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
CREATE TABLE user_meta_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_meta_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  data TEXT NOT NULL,
  tags TEXT DEFAULT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (user_meta_id) REFERENCES user_meta(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_user_meta_history_trigger
AFTER INSERT ON user_meta
BEGIN
  INSERT INTO user_meta_history (user_meta_id, user_id, data, tags, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.user_id, NEW.data, NEW.tags, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER user_meta_history_trigger
AFTER UPDATE ON user_meta
BEGIN
  INSERT INTO user_meta_history (user_meta_id, user_id, data, tags, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.user_id,  NEW.data, NEW.tags, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

CREATE TABLE file (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  url TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  --Foreign Keys
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE file_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  file_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  url TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (file_id) REFERENCES file(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_file_history_trigger
AFTER INSERT ON file
BEGIN
  INSERT INTO file_history(file_id, uuid, name, url, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.name, NEW.url, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER file_history_trigger
AFTER UPDATE ON file 
BEGIN
  INSERT INTO file_history (file_id, uuid, name, url, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.name, NEW.url, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;


CREATE TABLE token_session
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  user_id INTEGER NOT NULL,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user(id)
);


-- REFERENCE TABLES
----------------------------------------------

-- Create Table role
CREATE TABLE role (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  identifier TEXT NOT NULL,
  name TEXT NOT NULL
);
INSERT INTO role (identifier, name) VALUES ('admin', 'Admin');
INSERT INTO role (identifier, name) VALUES ('user', 'user');

