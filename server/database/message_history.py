import sqlite3


class MessageHistoryModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_message_history_by_id(self, cursor, message_history_id):
        """Retrieve a message history entry by its ID."""
        cursor.execute(
            """
            SELECT * FROM message_history WHERE id = ?
        """,
            (message_history_id,),
        )
        return cursor.fetchone()

    def get_message_history_by_er_id(self, cursor, user_id):
        """Retrieve all message history entries for a user."""
        cursor.execute(
            """
            SELECT * FROM message_history WHERE user_id = ?
        """,
            (user_id,),
        )
        return cursor.fetchall()
