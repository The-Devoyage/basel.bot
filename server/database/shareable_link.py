import logging
import sqlite3
import uuid
from datetime import datetime
from typing import Optional, Union
from classes.shareable_link import ShareableLink
from sqlite3 import Cursor
from classes.user import User

logger = logging.getLogger(__name__)


class ShareableLinkModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_shareable_link_by_id(
        self, cursor: Cursor, shareable_link_id: int
    ) -> Optional[ShareableLink]:
        cursor.execute(
            """
            SELECT * FROM shareable_link WHERE id = ?
            """,
            (shareable_link_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        logger.debug(f"SHAREABLE LINK FOUND: {data}")
        return ShareableLink(**data)

    def get_shareable_link_by_uuid(
        self, cursor: Cursor, shareable_link_uuid: str
    ) -> Optional[ShareableLink]:
        cursor.execute(
            """
            SELECT * FROM shareable_link WHERE uuid = ?
            """,
            (shareable_link_uuid,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        return ShareableLink(**data)

    def get_shareable_link_by_token(
        self, cursor: Cursor, token: str
    ) -> Optional[ShareableLink]:
        cursor.execute(
            """
            SELECT * FROM shareable_link WHERE token = ?
            """,
            (token,),
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

    def create_shareable_link(self, cursor: Cursor, user_id: int, tag: str):
        logger.debug("CREATING NEW SHAREABLE LINK")
        shareable_link_uuid = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO shareable_link (uuid, tag, created_by, updated_by)
            VALUES (?, ?, ?, ?)
            """,
            (shareable_link_uuid, tag, user_id, user_id),
        )
        logger.debug(f"NEW SHAREABLE LINK CREATED: {cursor.lastrowid}")
        return cursor.lastrowid

    def update_shareable_link(
        self,
        cursor: Cursor,
        current_user: User,
        shareable_link_id: int,
        token: Optional[str] = None,
        status: Optional[bool] = None,
        tag: Optional[str] = None,
    ):
        query = "UPDATE shareable_link SET updated_by = ?, updated_at = ?"
        bindings = (current_user.id, datetime.now())

        if token:
            query += ", token = ?"
            bindings += (token,)
        if status is not None:
            query += ", status = ?"
            bindings += (status,)
        if tag is not None:
            query += ", tag = ?"
            bindings += (tag,)

        query += " WHERE id = ?"

        cursor.execute(query, bindings + (shareable_link_id,))
        return cursor.rowcount
