-- Add up migration script here - sqlite

CREATE VIRTUAL TABLE product USING fts5(name, description);

CREATE TABLE product_meta (
  product_id INTEGER PRIMARY KEY REFERENCES product(id),
  url TEXT NOT NULL UNIQUE,
  thumbnail_url TEXT,
  status BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE product_category (
  product_id INTEGER NOT NULL REFERENCES product(id),
  category_id INTEGER NOT NULL REFERENCES category(id),
  PRIMARY KEY (product_id, category_id)
);

