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
        interview_id: int,
        limit: Union[int, None] = 10,
        offset: Union[int, None] = 0,
    ) -> list[InterviewQuestion]:
        cursor.execute(
            """
            SELECT * FROM interview_question WHERE interview_id = ? LIMIT ? OFFSET ?
            """,
            (
                interview_id,
                limit,
                offset,
            ),
        )
        columns = [column[0] for column in cursor.description]
        return [
            InterviewQuestion(**dict(zip(columns, row))) for row in cursor.fetchall()
        ]

    def create_interview_question(self, cursor: Cursor, user_id: int, question: str):
        logger.debug("CREATING NEW INTERVIEW QUESTION")
        interview_question_uuid = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO interview_question (uuid, question, created_by, updated_by)
            VALUES (?, ?, ?, ?)
            """,
            (interview_question_uuid, question, user_id, user_id),
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
