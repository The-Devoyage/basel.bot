import sqlite3
import uuid
from datetime import datetime


class UserProfileEducationModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_user_profile_education(
        self,
        cursor,
        user_profile_id,
        school,
        degree,
        field_of_study,
        start_date,
        end_date,
        description,
        created_by,
        updated_by,
    ):
        """Create a new user profile education entry with a generated UUID."""
        user_profile_education_uuid = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO user_profile_education (uuid, user_profile_id, school, degree, field_of_study, start_date, end_date, description, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                user_profile_education_uuid,
                user_profile_id,
                school,
                degree,
                field_of_study,
                start_date,
                end_date,
                description,
                created_by,
                updated_by,
            ),
        )
        return cursor.lastrowid

    def get_user_profile_education_by_id(self, cursor, user_profile_education_id):
        """Retrieve a user profile education entry by its ID."""
        cursor.execute(
            """
            SELECT * FROM user_profile_education WHERE id = ?
        """,
            (user_profile_education_id,),
        )
        return cursor.fetchone()

    def get_user_profile_education_by_user_profile_id(
        self, cursor, user_profile_id, limit=10
    ):
        """Retrieve all user profile education entries for a user profile."""
        cursor.execute(
            """
            SELECT * FROM user_profile_education WHERE user_profile_id = ? ORDER BY start_date DESC LIMIT ?
        """,
            (user_profile_id, limit),
        )
        return cursor.fetchall()

    def update_user_profile_education(
        self,
        cursor,
        user_profile_education_id,
        school,
        degree,
        field_of_study,
        start_date,
        end_date,
        description,
        updated_by,
    ):
        """Update a user profile education entry."""
        cursor.execute(
            """
            UPDATE user_profile_education
            SET school = ?, degree = ?, field_of_study = ?, start_date = ?, end_date = ?, description = ?, updated_by = ?, updated_at = ?
            WHERE id = ?
        """,
            (
                school,
                degree,
                field_of_study,
                start_date,
                end_date,
                description,
                updated_by,
                datetime.now(),
                user_profile_education_id,
            ),
        )
        return cursor.rowcount

    def delete_user_profile_education(
        self, cursor, user_profile_education_id, deleted_by
    ):
        """Soft delete a user profile education entry."""
        cursor.execute(
            """
            UPDATE user_profile_education
            SET deleted_by = ?, deleted_at = ?
            WHERE id = ?
        """,
            (deleted_by, datetime.now(), user_profile_education_id),
        )
        return cursor.rowcount
