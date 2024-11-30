-- Add up migration script here
CREATE TABLE interview(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE interview_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  interview_id INTEGER,
  uuid TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT DEFAULT NULL,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  -- Foreign Keys
  FOREIGN KEY (interview_id) REFERENCES interview(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_interview_history_trigger
AFTER INSERT ON interview
BEGIN
  INSERT INTO interview_history (interview_id, uuid, name, description, status, created_by, updated_by, deleted_by, created_at, updated_at, deleted_at)
  SELECT NEW.id, NEW.uuid, NEW.name, NEW.description, NEW.status, NEW.created_by, NEW.updated_by, NEW.deleted_by, NEW.created_at, NEW.updated_at, NEW.deleted_at;
END;

CREATE TRIGGER interview_history_trigger
AFTER UPDATE ON interview
BEGIN
  INSERT INTO interview_history (interview_id, uuid, name, description, status, created_by, updated_by, deleted_by, created_at, updated_at, deleted_at)
  SELECT NEW.id, NEW.uuid, NEW.name, NEW.description, NEW.status, NEW.created_by, NEW.updated_by, NEW.deleted_by, NEW.created_at, NEW.updated_at, NEW.deleted_at;
END;


-- Interview Question
CREATE TABLE interview_question(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  interview_id INTEGER NOT NULL,
  question TEXT NOT NULL,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (interview_id) REFERENCES interview(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE interview_question_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  interview_question_id INTEGER,
  uuid TEXT NOT NULL,
  interview_id INTEGER NOT NULL,
  question TEXT NOT NULL,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  -- Foreign Keys
  FOREIGN KEY (interview_question_id) REFERENCES interview_question(id),
  FOREIGN KEY (interview_id) REFERENCES interview(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_interview_question_history_trigger
AFTER INSERT ON interview_question
BEGIN
  INSERT INTO interview_question_history (interview_question_id, uuid, interview_id, question, status, created_by, updated_by, deleted_by, created_at, updated_at, deleted_at)
  SELECT NEW.id, NEW.uuid, NEW.interview_id, NEW.question, NEW.status, NEW.created_by, NEW.updated_by, NEW.deleted_by, NEW.created_at, NEW.updated_at, NEW.deleted_at;
END;

CREATE TRIGGER interview_question_history_trigger
AFTER UPDATE ON interview_question
BEGIN
  INSERT INTO interview_question_history (interview_question_id, uuid, interview_id, question, status, created_by, updated_by, deleted_by, created_at, updated_at, deleted_at)
  SELECT NEW.id, NEW.uuid, NEW.interview_id, NEW.question, NEW.status, NEW.created_by, NEW.updated_by, NEW.deleted_by, NEW.created_at, NEW.updated_at, NEW.deleted_at;
END;

-- Interview Question Response
CREATE TABLE interview_question_response(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  user_id INTEGER NOT NULL,
  interview_question_id INTEGER NOT NULL,
  response TEXT NOT NULL,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (interview_question_id) REFERENCES interview_question(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE interview_question_response_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  interview_question_response_id INTEGER,
  uuid TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  interview_question_id INTEGER NOT NULL,
  response TEXT NOT NULL,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  -- Foreign Keys
  FOREIGN KEY (interview_question_response_id) REFERENCES interview_question_response(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (interview_question_id) REFERENCES interview_question(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_interview_question_response_history_trigger
AFTER INSERT ON interview_question_response
BEGIN
  INSERT INTO interview_question_response_history (interview_question_response_id, uuid, user_id, interview_question_id, response, status, created_by, updated_by, deleted_by, created_at, updated_at, deleted_at)
  SELECT NEW.id, NEW.uuid, NEW.user_id, NEW.interview_question_id, NEW.response, NEW.status, NEW.created_by, NEW.updated_by, NEW.deleted_by, NEW.created_at, NEW.updated_at, NEW.deleted_at;
END;

CREATE TRIGGER interview_question_response_history_trigger
AFTER UPDATE ON interview_question_response
BEGIN
  INSERT INTO interview_question_response_history (interview_question_response_id, uuid, user_id, interview_question_id, response, status, created_by, updated_by, deleted_by, created_at, updated_at, deleted_at)
  SELECT NEW.id, NEW.uuid, NEW.user_id, NEW.interview_question_id, NEW.response, NEW.status, NEW.created_by, NEW.updated_by, NEW.deleted_by, NEW.created_at, NEW.updated_at, NEW.deleted_at;
END;

