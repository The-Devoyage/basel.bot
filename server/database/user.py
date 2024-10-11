import sqlite3
import uuid
from datetime import datetime

class UserModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_user(self, cursor, email, first_name, last_name, phone, role_id, created_by, updated_by, status=1, image=None):
        """Create a new user with a generated UUID."""
        user_uuid = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO user (uuid, email, first_name, last_name, phone, role_id, status, image, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_uuid, email, first_name, last_name, phone, role_id, status, image, created_by, updated_by))
        return cursor.lastrowid  # Return the newly created user's ID

    def get_user_by_id(self, cursor, user_id):
        """Retrieve a user by their ID."""
        cursor.execute("""
            SELECT * FROM user WHERE id = ?
        """, (user_id,))
        return cursor.fetchone()

    def update_user(self, cursor, user_id, email, first_name, last_name, phone, role_id, updated_by, status=1, image=None):
        """Update a user's information."""
        cursor.execute("""
            UPDATE user
            SET email = ?, first_name = ?, last_name = ?, phone = ?, role_id = ?, status = ?, image = ?, updated_by = ?, updated_at = ?
            WHERE id = ?
        """, (email, first_name, last_name, phone, role_id, status, image, updated_by, datetime.now(), user_id))
        return cursor.rowcount  # Return the number of rows updated

    def delete_user(self, cursor, user_id, deleted_by):
        """Soft delete a user."""
        cursor.execute("""
            UPDATE user
            SET deleted_by = ?, deleted_at = ?
            WHERE id = ?
        """, (deleted_by, datetime.now(), user_id))
        return cursor.rowcount  # Return the number of rows updated (soft delete)

