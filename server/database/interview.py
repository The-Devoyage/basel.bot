import logging
import sqlite3
import uuid
from datetime import datetime
from typing import Optional, Union
from sqlite3 import Cursor
from classes.interview import Interview
from classes.user import User

logger = logging.getLogger(__name__)


class InterviewModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_interview_by_id(
        self, cursor: Cursor, interview_id: int
    ) -> Optional[Interview]:
        cursor.execute(
            """
            SELECT * FROM interview WHERE id = ?
            """,
            (interview_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        logger.debug(f"INTERVIEW FOUND: {data}")
        return Interview(**data)

    def get_interview_by_uuid(
        self, cursor: Cursor, interview_uuid: str
    ) -> Optional[Interview]:
        cursor.execute(
            """
            SELECT * FROM interview WHERE uuid = ?
            """,
            (interview_uuid,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        return Interview(**data)

    def get_interviews(
        self,
        cursor: sqlite3.Cursor,
        name: Optional[str] = None,
        created_by: Optional[int] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ) -> list[Interview]:
        query = "SELECT * FROM interview WHERE deleted_at IS NULL"
        params = ()

        if name:
            wildcard = f"%{name}%"
            query += " AND name LIKE ?"
            params += (wildcard,)
        if created_by:
            query += " AND created_by = ?"
            params += (created_by,)

        query += " LIMIT ? OFFSET ?;"

        params += (
            limit,
            offset,
        )

        try:
            cursor.execute(query, params)
            columns = [column[0] for column in cursor.description]
            return [Interview(**dict(zip(columns, row))) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(e)
            raise e

    def create_interview(
        self, cursor: Cursor, user_id: int, name: str, description: str
    ):
        logger.debug("CREATING NEW INTERVIEW")
        interview_uuid = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO interview (uuid, name, description, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?)
            """,
            (interview_uuid, name, description, user_id, user_id),
        )
        logger.debug(f"NEW INTERVIEW CREATED: {cursor.lastrowid}")
        return cursor.lastrowid

    def update_interview(
        self,
        cursor: Cursor,
        current_user: User,
        interview_id: int,
        name: Optional[str] = None,
        description: Optional[bool] = None,
        status: Optional[bool] = None,
    ):
        query = "UPDATE interview SET updated_by = ?, updated_at = ?"
        bindings = (current_user.id, datetime.now())

        if name:
            query += ", name = ?"
            bindings += (name,)
        if description:
            query += ", description = ?"
            bindings += (description,)
        if status is not None:
            query = ", status = ?"
            bindings += (status,)

        query += " WHERE id = ?"

        cursor.execute(query, bindings + (interview_id,))
        return cursor.rowcount
