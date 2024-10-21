import sqlite3
import uuid
from datetime import datetime
from typing import Optional
import logging
from classes.token_session import TokenSession

from classes.user import User


logger = logging.getLogger(__name__)


class TokenSessionModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_token_session(
        self,
        cursor,
        user_id,
    ) -> int:
        """Create a new token session with a generated UUID."""
        cursor.execute(
            """
            INSERT INTO token_session (user_id, uuid, created_at)
            VALUES (?, ?, ?)
        """,
            (
                user_id,
                str(uuid.uuid4()),
                datetime.now(),
            ),
        )
        return cursor.lastrowid  # Return the newly created token session's ID

    def get_token_session_by_id(
        self, cursor, token_session_id
    ) -> Optional[TokenSession]:
        """Retrieve a token session by its ID."""
        cursor.execute(
            """
            SELECT * FROM token_session WHERE id = ?
        """,
            (token_session_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        try:
            return TokenSession(**dict(zip(columns, row)))
        except Exception as e:
            logger.error(e)
            return None

    def get_token_session_by_uuid(self, cursor, uuid) -> Optional[TokenSession]:
        """Retrieve a token session by its uuid."""
        cursor.execute(
            """
            SELECT * FROM token_session WHERE uuid = ?
        """,
            (uuid,),
        )
        row = cursor.fetchone()

        if not row:
            return None

        columns = [column[0] for column in cursor.description]

        try:
            return TokenSession(**dict(zip(columns, row)))
        except Exception as e:
            logger.error(e)
            return None

    def invalidate_token_session(self, cursor, token_session_uuid) -> bool:
        """Invalidate a token session."""
        cursor.execute(
            """
            UPDATE token_session SET status = 0 WHERE uuid = ?
        """,
            (token_session_uuid,),
        )
        return cursor.rowcount > 0
