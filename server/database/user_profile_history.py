import sqlite3


class UserProfileHistoryModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_user_profile_history_by_id(self, cursor, user_profile_history_id):
        """Retrieve a user profile history entry by its ID."""
        cursor.execute(
            """
            SELECT * FROM user_profile_history WHERE id = ?
            """,
            (user_profile_history_id,),
        )
        return cursor.fetchone()

    def get_user_profile_history_by_user_id(self, cursor, user_id, limit=10):
        """Retrieve all user history entries for a user."""
        cursor.execute(
            """
            SELECT * FROM user_profile_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?
            """,
            (user_id, limit),
        )
        return cursor.fetchall()
