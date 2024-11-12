import sqlite3
import uuid
from datetime import datetime
from typing import Optional
import logging
from classes.subscription import Subscription

logger = logging.getLogger(__name__)


class SubscriptionModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_subscription(self, cursor: sqlite3.Cursor, user_id: int) -> int | None:
        cursor.execute(
            """
                       INSERT INTO subscription(user_id, uuid)
                       VALUES (?, ?)
                       """,
            (
                user_id,
                str(
                    uuid.uuid4(),
                ),
            ),
        )
        return cursor.lastrowid

    def get_subscription_by_id(
        self, cursor: sqlite3.Cursor, id: int
    ) -> Subscription | None:
        cursor.execute(
            """
                       SELECT * FROM subscription WHERE id = ?
                       """,
            (id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        logger.debug(f"SUBSCRIPTION FOUND: {data}")
        return Subscription(**data)
