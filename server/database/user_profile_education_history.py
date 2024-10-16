import sqlite3


class UserProfileEducationHistoryModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_user_profile_education_history_by_id(
        self, cursor, user_profile_education_history_id
    ):
        """Retrieve a user profile education history entry by its ID."""
        cursor.execute(
            """
            SELECT * FROM user_profile_education_history WHERE id = ?
        """,
            (user_profile_education_history_id,),
        )
        return cursor.fetchone()

    def get_user_profile_education_history_by_user_id(self, cursor, user_id):
        """Retrieve all user profile education history entries for a user."""
        cursor.execute(
            """
            SELECT * FROM user_profile_education_history WHERE user_id = ?
        """,
            (user_id,),
        )
        return cursor.fetchall()
