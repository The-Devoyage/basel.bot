-- Add up migration script here

CREATE TABLE profile_picture (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  filename TEXT NOT NULL,
  file_extension TEXT NOT NULL,
  file_path TEXT NOT NULL,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);

CREATE TABLE profile_picture_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  profile_picture_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  filename TEXT NOT NULL,
  file_extension TEXT NOT NULL,
  file_path TEXT NOT NULL,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (profile_picture_id) REFERENCES profile_picture(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);

CREATE TRIGGER new_profile_picture_history_trigger
AFTER INSERT ON profile_picture
BEGIN
  INSERT INTO profile_picture_history (profile_picture_id, user_id, filename, file_extension, file_path, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.user_id, NEW.filename, NEW.file_extension, NEW.file_path, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

CREATE TRIGGER profile_picture_history_trigger
AFTER UPDATE ON profile_picture
BEGIN
  INSERT INTO profile_picture_history (profile_picture_id, user_id, filename, file_extension, file_path, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.user_id, NEW.filename, NEW.file_extension, NEW.file_path, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
