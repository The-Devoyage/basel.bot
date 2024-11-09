import sqlite3
from typing import List
import uuid
from datetime import datetime
from classes.message import Message


class MessageModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_message(self, cursor, user_id, sender, text, created_by, updated_by):
        """Create a new message with a generated UUID, using the provided cursor."""
        message_uuid = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO message (uuid, user_id, sender, text, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (message_uuid, user_id, sender, text, created_by, updated_by),
        )
        return cursor.lastrowid  # Return the newly created message's ID

    def get_message_by_id(self, cursor, message_id):
        """Retrieve a message by its ID using the provided cursor."""
        cursor.execute(
            """
            SELECT * FROM message WHERE id = ?
        """,
            (message_id,),
        )
        return cursor.fetchone()

    def get_messages_by_user_id(self, cursor, user_id, created_at) -> List[Message]:
        """Retrieve all messages by a user using the provided cursor."""
        cursor.execute(
            """
            SELECT * FROM message WHERE user_id = ? AND created_at > ?
        """,
            (user_id, created_at),
        )
        columns = [column[0] for column in cursor.description]
        return [Message(**dict(zip(columns, row))) for row in cursor.fetchall()]

    def update_message(self, cursor, message_id, text, updated_by):
        """Update a message's text using the provided cursor."""
        cursor.execute(
            """
            UPDATE message
            SET text = ?, updated_by = ?, updated_at = ?
            WHERE id = ?
        """,
            (text, updated_by, datetime.now(), message_id),
        )
        return cursor.rowcount  # Number of rows updated

    def delete_message(self, cursor, message_id, deleted_by):
        """Soft delete a message using the provided cursor."""
        cursor.execute(
            """
            UPDATE message
            SET deleted_by = ?, deleted_at = ?
            WHERE id = ?
        """,
            (deleted_by, datetime.now(), message_id),
        )
        return cursor.rowcount  # Number of rows updated (soft deleted)
