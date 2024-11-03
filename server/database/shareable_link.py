import sqlite3
import uuid
from typing import Optional, Union
from classes.shareable_link import ShareableLink


class ShareableLinkModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_shareable_link_by_id(
        self, cursor: sqlite3.Cursor, shareable_link_id: int, user_id: int
    ) -> Optional[ShareableLink]:
        cursor.execute(
            """
            SELECT * FROM shareable_link WHERE id = ? AND created_by = ?
            """,
            (
                shareable_link_id,
                user_id,
            ),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        return ShareableLink(**data)

    def get_shareable_links(
        self,
        cursor,
        user_id,
        limit: Union[int, None] = 10,
        offset: Union[int, None] = 0,
    ) -> list[ShareableLink]:
        cursor.execute(
            """
            SELECT * FROM shareable_link WHERE created_by = ? LIMIT ? OFFSET ?
            """,
            (
                user_id,
                limit,
                offset,
            ),
        )
        columns = [column[0] for column in cursor.description]
        return [ShareableLink(**dict(zip(columns, row))) for row in cursor.fetchall()]

    def create_shareable_link(self, cursor: sqlite3.Cursor, user_id: int, tag: str):
        shareable_link_uuid = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO shareable_link (uuid, tag, created_by, updated_by)
            VALUES (?, ?, ?, ?)
            """,
            (shareable_link_uuid, tag, user_id, user_id),
        )
        return cursor.lastrowid

    def update_shareable_link(self, cursor, shareable_link_id, token) -> int:
        cursor.execute(
            """
                UPDATE shareable_link SET token = ? WHERE id = ?
            """,
            (
                token,
                shareable_link_id,
            ),
        )
        return cursor.lastrowid
