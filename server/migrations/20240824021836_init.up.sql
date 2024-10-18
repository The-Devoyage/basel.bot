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
  file INTEGER,
  auth_id TEXT NOT NULL,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (file) REFERENCES file(id),
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
  file INTEGER,
  auth_id TEXT NOT NULL,
  created_by INTEGER DEFAULT NULL,
  updated_by INTEGER DEFAULT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (file) REFERENCES file(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (role_id) REFERENCES role(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_user_history_trigger
AFTER INSERT ON user
BEGIN
  INSERT INTO user_history (user_id, uuid, email, first_name, last_name, phone, role_id, status, file, auth_id, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.email, NEW.first_name, NEW.last_name, NEW.phone, NEW.role_id, NEW.status, NEW.file, NEW.auth_id, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER user_history_trigger
AFTER UPDATE ON user
BEGIN
  INSERT INTO user_history (user_id, uuid, email, first_name, last_name, phone, role_id, status, file, auth_id, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.email, NEW.first_name, NEW.last_name, NEW.phone, NEW.role_id, NEW.status, NEW.file, NEW.auth_id, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

-- Create Table user_profile
CREATE TABLE user_profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  user_id INTEGER NOT NULL,
  title TEXT,
  summary TEXT,
  location TEXT,
  website TEXT,
  github TEXT,
  linkedin TEXT,
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
CREATE TABLE user_profile_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  user_profile_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  title TEXT,
  summary TEXT,
  location TEXT,
  website TEXT,
  github TEXT,
  linkedin TEXT,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (user_profile_id) REFERENCES user_profile(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_user_profile_history_trigger
AFTER INSERT ON user_profile
BEGIN
  INSERT INTO user_profile_history (user_profile_id, uuid, user_id, title, summary, location, website, github, linkedin, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.user_id, NEW.title, NEW.summary, NEW.location, NEW.website, NEW.github, NEW.linkedin, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER user_profile_history_trigger
AFTER UPDATE ON user_profile
BEGIN
  INSERT INTO user_profile_history (user_profile_id, uuid, user_id, title, summary, location, website, github, linkedin, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.user_id, NEW.title, NEW.summary, NEW.location, NEW.website, NEW.github, NEW.linkedin, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

-- Create Table User Education
CREATE TABLE user_profile_education (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  user_profile_id INTEGER NOT NULL,
  school TEXT NOT NULL,
  degree TEXT NOT NULL,
  field_of_study TEXT NOT NULL,
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL,
  description TEXT,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (user_profile_id) REFERENCES user_profile(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE user_profile_education_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  user_profile_education_id INTEGER NOT NULL,
  user_profile_id INTEGER NOT NULL,
  school TEXT NOT NULL,
  degree TEXT NOT NULL,
  field_of_study TEXT NOT NULL,
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL,
  description TEXT,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (user_profile_education_id) REFERENCES user_profile_education(id),
  FOREIGN KEY (user_profile_id) REFERENCES user_profile(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_user_profile_education_history_trigger
AFTER INSERT ON user_profile_education
BEGIN
  INSERT INTO user_profile_education_history (user_profile_education_id, uuid, user_profile_id, school, degree, field_of_study, start_date, end_date, description, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.user_profile_id, NEW.school, NEW.degree, NEW.field_of_study, NEW.start_date, NEW.end_date, NEW.description, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER user_profile_education_history_trigger
AFTER UPDATE ON user_profile_education
BEGIN
  INSERT INTO user_profile_education_history (user_profile_education_id, uuid, user_profile_id, school, degree, field_of_study, start_date, end_date, description, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.user_profile_id, NEW.school, NEW.degree, NEW.field_of_study, NEW.start_date, NEW.end_date, NEW.description, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

-- Create Table organization
CREATE TABLE organization (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  description TEXT,
  file INTEGER,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (file) REFERENCES file(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE organization_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  organization_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  file INTEGER,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (file) REFERENCES file(id),
  FOREIGN KEY (organization_id) REFERENCES organization(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_organization_history_trigger
AFTER INSERT ON organization
BEGIN
  INSERT INTO organization_history (organization_id, uuid, name, description, file, status, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.name, NEW.description, NEW.file, NEW.status, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER organization_history_trigger
AFTER UPDATE ON organization
BEGIN
  INSERT INTO organization_history (organization_id, uuid, name, description, file, status, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.name, NEW.description, NEW.file, NEW.status, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

-- Create Table organization_user
CREATE TABLE organization_user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  organization_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  edit_posting BOOLEAN NOT NULL DEFAULT 0,
  delete_posting BOOLEAN NOT NULL DEFAULT 0,
  create_posting BOOLEAN NOT NULL DEFAULT 0,
  manage_application BOOLEAN NOT NULL DEFAULT 0,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (organization_id) REFERENCES organization(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE organization_user_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  organization_user_id INTEGER NOT NULL,
  organization_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  edit_posting BOOLEAN NOT NULL DEFAULT 0,
  delete_posting BOOLEAN NOT NULL DEFAULT 0,
  create_posting BOOLEAN NOT NULL DEFAULT 0,
  manage_application BOOLEAN NOT NULL DEFAULT 0,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (organization_user_id) REFERENCES organization_user(id),
  FOREIGN KEY (organization_id) REFERENCES organization(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_organization_user_history_trigger
AFTER INSERT ON organization_user
BEGIN
  INSERT INTO organization_user_history (organization_user_id, uuid, organization_id, user_id, edit_posting, delete_posting, create_posting, manage_application, status, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.organization_id, NEW.uuid, NEW.user_id, NEW.edit_posting, NEW.delete_posting, NEW.create_posting, NEW.manage_application, NEW.status, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER organization_user_history_trigger
AFTER UPDATE ON organization_user
BEGIN
  INSERT INTO organization_user_history (organization_user_id, uuid, organization_id, user_id, edit_posting, delete_posting, create_posting, manage_application, status, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.organization_id, NEW.uuid, NEW.user_id, NEW.edit_posting, NEW.delete_posting, NEW.create_posting, NEW.manage_application, NEW.status, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

-- Create Table posting
CREATE TABLE posting (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  organization_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (organization_id) REFERENCES organization(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE posting_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  posting_id INTEGER NOT NULL,
  organization_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  status BOOLEAN NOT NULL DEFAULT 1,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (posting_id) REFERENCES posting(id),
  FOREIGN KEY (organization_id) REFERENCES organization(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_posting_history_trigger
AFTER INSERT ON posting
BEGIN
  INSERT INTO posting_history (posting_id, uuid, organization_id, title, description, status, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.organization_id, NEW.title, NEW.description, NEW.status, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER posting_history_trigger
AFTER UPDATE ON posting
BEGIN
  INSERT INTO posting_history (posting_id, uuid, organization_id, title, description, status, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.organization_id, NEW.title, NEW.description, NEW.status, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

-- Create Table application
CREATE TABLE application (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  posting_id INTEGER NOT NULL,
  user_profile_id INTEGER NOT NULL,
  status_id INTEGER NOT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (posting_id) REFERENCES posting(id),
  FOREIGN KEY (user_profile_id) REFERENCES user_profile(id),
  FOREIGN KEY (status_id) REFERENCES application_status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TABLE application_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  application_id INTEGER NOT NULL,
  posting_id INTEGER NOT NULL,
  user_profile_id INTEGER NOT NULL,
  status_id INTEGER NOT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  --Foreign Keys
  FOREIGN KEY (application_id) REFERENCES application(id),
  FOREIGN KEY (posting_id) REFERENCES posting(id),
  FOREIGN KEY (user_profile_id) REFERENCES user_profile(id),
  FOREIGN KEY (status_id) REFERENCES application_status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_application_history_trigger
AFTER INSERT ON application
BEGIN
  INSERT INTO application_history (application_id, uuid, posting_id, user_profile_id, status_id, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.posting_id, NEW.user_profile_id, NEW.status_id, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER application_history_trigger
AFTER UPDATE ON application
BEGIN
  INSERT INTO application_history (application_id, uuid, posting_id, user_profile_id, status_id, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.posting_id, NEW.user_profile_id, NEW.status_id, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
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


-- Create table posting_skill
CREATE TABLE posting_skill (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  posting_id INTEGER NOT NULL,
  skill_id INTEGER NOT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (posting_id) REFERENCES posting(id),
  FOREIGN KEY (skill_id) REFERENCES skill(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id),
  UNIQUE(posting_id, skill_id)
);
CREATE TABLE posting_skill_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  posting_skill_id INTEGER NOT NULL,
  posting_id INTEGER NOT NULL,
  skill_id INTEGER NOT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (posting_skill_id) REFERENCES posting_skill(id),
  FOREIGN KEY (posting_id) REFERENCES posting(id),
  FOREIGN KEY (skill_id) REFERENCES skill(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_posting_skill_history_trigger
AFTER INSERT ON posting_skill
BEGIN
  INSERT INTO posting_skill_history (posting_skill_id, uuid, posting_id, skill_id, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.posting_id, NEW.skill_id, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER posting_skill_history_trigger
AFTER UPDATE ON posting_skill
BEGIN
  INSERT INTO posting_skill_history (posting_skill_id, uuid, posting_id, skill_id, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.posting_id, NEW.skill_id, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END; 

-- Create table user_profile_skill
CREATE TABLE user_profile_skill (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL UNIQUE,
  user_profile_id INTEGER NOT NULL,
  skill_id INTEGER NOT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (user_profile_id) REFERENCES user_profile(id),
  FOREIGN KEY (skill_id) REFERENCES skill(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id),
  UNIQUE(user_profile_id, skill_id)
);
CREATE TABLE user_profile_skill_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid TEXT NOT NULL,
  user_skill_id INTEGER NOT NULL,
  user_profile_id INTEGER NOT NULL,
  skill_id INTEGER NOT NULL,
  created_by INTEGER NOT NULL,
  updated_by INTEGER NOT NULL,
  deleted_by INTEGER DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (user_skill_id) REFERENCES user_skill(id),
  FOREIGN KEY (user_profile_id) REFERENCES user_profile(id),
  FOREIGN KEY (skill_id) REFERENCES skill(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  FOREIGN KEY (deleted_by) REFERENCES user(id)
);
CREATE TRIGGER new_user_profile_skill_history_trigger
AFTER INSERT ON user_profile_skill
BEGIN
  INSERT INTO user_skill_history (user_profile_skill_id, uuid, user_profile_id, skill_id, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.user_profile_id, NEW.skill_id, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;
CREATE TRIGGER user_profile_skill_history_trigger
AFTER UPDATE ON user_profile_skill
BEGIN
  INSERT INTO user_skill_history (user_profile_skill_id, uuid, user_profile_id, skill_id, created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
  SELECT NEW.id, NEW.uuid, NEW.user_profile_id, NEW.skill_id, NEW.created_at, NEW.updated_at, NEW.created_by, NEW.updated_by, NEW.deleted_at, NEW.deleted_by;
END;

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

-- Create table application_status
CREATE TABLE application_status (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  identifier TEXT NOT NULL
);
INSERT INTO application_status (name, identifier) VALUES ('Pending', 'pending');
INSERT INTO application_status (name, identifier) VALUES ('Accepted', 'accepted');
INSERT INTO application_status (name, identifier) VALUES ('Rejected', 'rejected');


-- Create Table skill
CREATE TABLE skill (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  identifier TEXT NOT NULL
);
  
INSERT INTO skill (name, identifier) 
VALUES 
  ('Java', 'java'),
  ('Python', 'python'),
  ('JavaScript', 'javascript'),
  ('C++', 'c++'),
  ('C#', 'c#'),
  ('Ruby', 'ruby'),
  ('PHP', 'php'),
  ('Swift', 'swift'),
  ('Kotlin', 'kotlin'),
  ('Go', 'go'),
  ('Rust', 'rust'),
  ('TypeScript', 'typescript'),
  ('SQL', 'sql'),
  ('NoSQL', 'nosql'),
  ('Docker', 'docker'),
  ('Kubernetes', 'kubernetes'),
  ('AWS', 'aws'),
  ('Azure', 'azure'),
  ('GCP', 'gcp'),
  ('Firebase', 'firebase'),
  ('React', 'react'),
  ('Angular', 'angular'),
  ('Vue', 'vue'),
  ('Node.js', 'nodejs'),
  ('Express', 'express'),
  ('Flask', 'flask'),
  ('Django', 'django'),
  ('Spring', 'spring'),
  ('Laravel', 'laravel'),
  ('Symfony', 'symfony'),
  ('Ruby on Rails', 'ruby-on-rails'),
  ('ASP.NET', 'asp.net'),
  ('Android', 'android'),
  ('iOS', 'ios'),
  ('React Native', 'react-native'),
  ('Flutter', 'flutter'),
  ('Xamarin', 'xamarin'),
  ('Unity', 'unity'),
  ('Unreal Engine', 'unreal-engine'),
  ('Machine Learning', 'machine-learning'),
  ('Deep Learning', 'deep-learning'),
  ('Data Science', 'data-science'),
  ('Big Data', 'big-data'),
  ('DevOps', 'devops'),
  ('Cybersecurity', 'cybersecurity'),
  ('Blockchain', 'blockchain'),
  ('IoT', 'iot'),
  ('AR/VR', 'ar-vr'),
  ('Game Development', 'game-development'),
  ('Web Development', 'web-development'),
  ('Mobile Development', 'mobile-development'),
  ('Desktop Development', 'desktop-development'),
  ('Cloud Computing', 'cloud-computing'),
  ('Database Management', 'database-management'),
  ('Frontend Development', 'frontend-development'),
  ('Backend Development', 'backend-development'),
  ('Fullstack Development', 'fullstack-development'),
  ('Software Development', 'software-development'),
  ('Hardware Development', 'hardware-development'),
  ('Network Development', 'network-development'),
  ('Security Development', 'security-development'),
  ('Quality Assurance', 'quality-assurance'),
  ('Project Management', 'project-management'),
  ('Product Management', 'product-management'),
  ('Business Analysis', 'business-analysis'),
  ('Data Analysis', 'data-analysis'),
  ('UI/UX Design', 'ui-ux-design'),
  ('Graphic Design', 'graphic-design'),
  ('Motion Design', 'motion-design'),
  ('3D Design', '3d-design'),
  ('Video Editing', 'video-editing'),
  ('Photography', 'photography'),
  ('Illustration', 'illustration'),
  ('Animation', 'animation'),
  ('Music Production', 'music-production'),
  ('Sound Design', 'sound-design'),
  ('Voice Acting', 'voice-acting'),
  ('Writing', 'writing');
