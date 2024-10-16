import sqlite3
import uuid
from datetime import datetime


class UserProfileSkillModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_user_profile_skill(
        self, cursor, user_profile_id, skill_id, created_by, updated_by
    ):
        """Create a new user profile skill."""
        user_profile_skill_uuid = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO user_profile_skill (uuid, user_profile_id, skill_id, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                user_profile_skill_uuid,
                user_profile_id,
                skill_id,
                created_by,
                updated_by,
            ),
        )
        return cursor.lastrowid

    def get_user_profile_skill_by_id(self, cursor, user_profile_skill_id):
        """Retrieve a user profile skill by its ID."""
        cursor.execute(
            """
            SELECT * FROM user_profile_skill WHERE id = ?
        """,
            (user_profile_skill_id,),
        )
        return cursor.fetchone()

    def update_user_profile_skill(
        self, cursor, user_profile_skill_id, skill_id, updated_by
    ):
        """Update a user profile skill."""
        cursor.execute(
            """
            UPDATE user_profile_skill
            SET skill_id = ?, updated_by = ?, updated_at = ?
            WHERE id = ?
        """,
            (skill_id, updated_by, datetime.now(), user_profile_skill_id),
        )
        return cursor.rowcount

    def delete_user_profile_skill(self, cursor, user_profile_skill_id, deleted_by):
        """Soft delete a user profile skill."""
        cursor.execute(
            """
            UPDATE user_profile_skill
            SET deleted_by = ?, deleted_at = ?
            WHERE id = ?
        """,
            (deleted_by, datetime.now(), user_profile_skill_id),
        )
        return cursor.rowcount
