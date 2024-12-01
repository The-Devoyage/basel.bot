import logging
import sqlite3
import uuid
from datetime import datetime
from typing import Optional, Union
from sqlite3 import Cursor
from classes.interview_question import InterviewQuestion
from classes.user import User

logger = logging.getLogger(__name__)


class InterviewQuestionModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_interview_question_by_id(
        self, cursor: Cursor, interview_question_id: int
    ) -> Optional[InterviewQuestion]:
        cursor.execute(
            """
            SELECT * FROM interview_question WHERE id = ?
            """,
            (interview_question_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        logger.debug(f"INTERVIEW QUESTION FOUND: {data}")
        return InterviewQuestion(**data)

    def get_interview_question_by_uuid(
        self, cursor: Cursor, interview_question_uuid: str
    ) -> Optional[InterviewQuestion]:
        cursor.execute(
            """
            SELECT * FROM interview_question WHERE uuid = ?
            """,
            (interview_question_uuid,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        return InterviewQuestion(**data)

    def get_interview_questions(
        self,
        cursor,
        interview_id: Optional[int] = None,
        interview_uuid: Optional[str] = None,
        limit: Union[int, None] = 10,
        offset: Union[int, None] = 0,
    ) -> list[InterviewQuestion]:
        query = "SELECT * FROM interview_question WHERE deleted_at IS NULL"
        params = ()

        if interview_id:
            query += " AND id = ?"
            params += (interview_id,)
        if interview_uuid:
            query += " AND interview_id = (SELECT id FROM interview WHERE uuid = ?)"
            params += (interview_uuid,)

        query += " LIMIT ? OFFSET ?"
        params += (limit, offset)

        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        return [
            InterviewQuestion(**dict(zip(columns, row))) for row in cursor.fetchall()
        ]

    def create_interview_question(
        self, cursor: Cursor, user_id: int, interview_uuid: str, question: str
    ):
        logger.debug("CREATING NEW INTERVIEW QUESTION")
        interview_question_uuid = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO interview_question (uuid, interview_id, question, created_by, updated_by)
            VALUES (?, (SELECT id FROM interview WHERE uuid = ?), ?, ?, ?)
            """,
            (interview_question_uuid, interview_uuid, question, user_id, user_id),
        )
        logger.debug(f"NEW INTERVIEW QUESTION CREATED: {cursor.lastrowid}")
        return cursor.lastrowid

    def update_interview_question(
        self,
        cursor: Cursor,
        current_user: User,
        interview_question_id: int,
        question: Optional[str] = None,
        status: Optional[bool] = None,
    ):
        query = "UPDATE interview_question SET updated_by = ?, updated_at = ?"
        bindings = (current_user.id, datetime.now())

        if question:
            query += ", question = ?"
            bindings += (question,)
        if status is not None:
            query += ", status = ?"
            bindings += (status,)

        query += " WHERE id = ?"

        cursor.execute(query, bindings + (interview_question_id,))
        return cursor.rowcount
