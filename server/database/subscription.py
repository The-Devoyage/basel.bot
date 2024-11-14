import sqlite3
from typing import List
import uuid
from classes.subscription import Subscription


class SubscriptionModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_subscription(
        self, cursor: sqlite3.Cursor, user_id: int, checkout_session_id: str
    ) -> int | None:
        cursor.execute(
            """
                       INSERT INTO subscription(uuid, user_id, checkout_session_id)
                       VALUES (?, ?, ?)
                       """,
            (
                str(
                    uuid.uuid4(),
                ),
                user_id,
                checkout_session_id,
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
        return Subscription(**data)

    def get_subscriptions_by_user_id(
        self, cursor: sqlite3.Cursor, user_id: int, active: bool = True
    ) -> List[Subscription]:
        cursor.execute(
            "SELECT * FROM subscription WHERE user_id = ? AND status = ?",
            (user_id, active),
        )
        columns = [column[0] for column in cursor.description]
        return [Subscription(**dict(zip(columns, row))) for row in cursor.fetchall()]

    def get_subscription_by_checkout_session_id(
        self, cursor: sqlite3.Cursor, checkout_session_id: str
    ) -> Subscription | None:
        cursor.execute(
            """
                       SELECT * FROM subscription WHERE checkout_session_id = ?
                       """,
            (checkout_session_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))
        return Subscription(**data)

    def update_subscription(
        self, cursor: sqlite3.Cursor, checkout_session_id: str, status: bool
    ) -> int | None:
        cursor.execute(
            """
                       UPDATE subscription SET status = ? WHERE checkout_session_id = ?
                       """,
            (
                status,
                checkout_session_id,
            ),
        )
        return cursor.rowcount
