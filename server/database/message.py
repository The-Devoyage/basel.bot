import logging
import sqlite3
from typing import List, Optional
import uuid
from datetime import datetime
from classes.message import Message, SenderIdentifer

logger = logging.getLogger(__name__)


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

    def get_messages(
        self,
        cursor: sqlite3.Cursor,
        user_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        sender: Optional[SenderIdentifer] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ) -> List[Message]:
        """Retrieve all messages by a user using the provided cursor."""
        query = "SELECT * FROM (SELECT * FROM message WHERE deleted_at IS NULL"
        params = ()

        if user_id:
            query += " AND user_id = ?"
            params += (user_id,)
        if created_at:
            query += " AND created_at >= ?"
            params += (created_at,)
        if sender:
            query += " AND sender = ?"
            params += (sender,)

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params += (
            limit,
            offset,
        )

        query += ") sub ORDER BY created_at ASC;"

        logger.debug(f"QUERY: {query}")

        cursor.execute(query, params)
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
