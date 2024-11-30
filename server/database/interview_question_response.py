import logging
import sqlite3
import uuid
from typing import Optional, Union
from sqlite3 import Cursor
from classes.interview_question_response import InterviewQuestionResponse

logger = logging.getLogger(__name__)


class InterviewQuestionResponseModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_interview_question_response_by_id(
        self, cursor: Cursor, interview_question_response_id: int
    ) -> Optional[InterviewQuestionResponse]:
        cursor.execute(
            """
            SELECT * FROM interview_question_response WHERE id = ?
            """,
            (interview_question_response_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        logger.debug(f"INTERVIEW QUESTION RESPONSE FOUND: {data}")
        return InterviewQuestionResponse(**data)

    def get_interview_question_response_by_uuid(
        self, cursor: Cursor, interview_question_response_uuid: str
    ) -> Optional[InterviewQuestionResponse]:
        cursor.execute(
            """
            SELECT * FROM interview_question_response WHERE uuid = ?
            """,
            (interview_question_response_uuid,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        return InterviewQuestionResponse(**data)

    def get_interview_question_responses(
        self,
        cursor,
        interview_id: int,
        limit: Union[int, None] = 10,
        offset: Union[int, None] = 0,
    ) -> list[InterviewQuestionResponse]:
        cursor.execute(
            """
            SELECT * FROM interview_question_response WHERE interview_id = ? LIMIT ? OFFSET ?
            """,
            (
                interview_id,
                limit,
                offset,
            ),
        )
        columns = [column[0] for column in cursor.description]
        return [
            InterviewQuestionResponse(**dict(zip(columns, row)))
            for row in cursor.fetchall()
        ]

    def create_interview_question_response(
        self, cursor: Cursor, user_id: int, response: str
    ):
        logger.debug("CREATING NEW INTERVIEW QUESTION RESPONSE")
        interview_question_response_uuid = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO interview_question_response (uuid, user_id, response, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?)
            """,
            (interview_question_response_uuid, user_id, response, user_id, user_id),
        )
        logger.debug(f"NEW INTERVIEW QUESTION RESPONSE CREATED: {cursor.lastrowid}")
        return cursor.lastrowid
