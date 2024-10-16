import sqlite3
import uuid
from datetime import datetime


class UserProfileModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_user_profile(
        self,
        cursor,
        user_id,
        title,
        summary,
        location,
        website,
        github,
        linkedin,
        created_by,
        updated_by,
    ):
        """Create a new user profile with a generated UUID."""
        user_profile_uuid = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO user_profile (uuid, user_id, title, summary, location, website, github, linkedin, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                user_profile_uuid,
                user_id,
                title,
                summary,
                location,
                website,
                github,
                linkedin,
                created_by,
                updated_by,
            ),
        )
        return cursor.lastrowid

    def get_user_profile_by_id(self, cursor, user_profile_id):
        """Retrieve a user profile by its ID."""
        cursor.execute(
            """
            SELECT * FROM user_profile WHERE id = ?
        """,
            (user_profile_id,),
        )
        return cursor.fetchone()

    def update_user_profile(
        self,
        cursor,
        user_profile_id,
        title,
        summary,
        location,
        website,
        github,
        linkedin,
        updated_by,
    ):
        """Update a user profile's information."""
        cursor.execute(
            """
            UPDATE user_profile
            SET title = ?, summary = ?, location = ?, website = ?, github = ?, linkedin = ?, updated_by = ?, updated_at = ?
            WHERE id = ?
        """,
            (
                title,
                summary,
                location,
                website,
                github,
                linkedin,
                updated_by,
                datetime.now(),
                user_profile_id,
            ),
        )
        return cursor.rowcount

    def delete_user_profile(self, cursor, user_profile_id, deleted_by):
        """Soft delete a user profile."""
        cursor.execute(
            """
            UPDATE user_profile
            SET deleted_by = ?, deleted_at = ?
            WHERE id = ?
        """,
            (deleted_by, datetime.now(), user_profile_id),
        )
        return cursor.rowcount
