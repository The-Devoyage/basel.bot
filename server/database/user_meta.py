import sqlite3
import logging

logger = logging.getLogger(__name__)


class UserMetaModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_user_meta(
        self,
        cursor,
        user_id,
        tags,
        data,
        current_user_id,
    ) -> int:
        logger.debug("INSERTING USER META")
        cursor.execute(
            """
            INSERT INTO user_meta (user_id, `data`, tags, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?)
        """,
            (user_id, data, tags, current_user_id, current_user_id),
        )
        return cursor.lastrowid
