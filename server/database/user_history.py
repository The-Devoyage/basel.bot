import sqlite3


class UserHistoryModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_user_history_by_id(self, cursor, user_history_id):
        """Retrieve a user history entry by its ID."""
        cursor.execute(
            """
            SELECT * FROM user_history WHERE id = ?
        """,
            (user_history_id,),
        )
        return cursor.fetchone()

    def get_user_history_by_user_id(self, cursor, user_id):
        """Retrieve all user history entries for a user."""
        cursor.execute(
            """
            SELECT * FROM user_history WHERE user_id = ?
        """,
            (user_id,),
        )
        return cursor.fetchall()
