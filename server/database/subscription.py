from datetime import datetime
import sqlite3
from typing import List, Optional
import uuid
from classes.subscription import Subscription


class SubscriptionModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_subscription(
        self,
        cursor: sqlite3.Cursor,
        user_id: int,
        checkout_session_id: str,
    ) -> int | None:
        cursor.execute(
            """
                       INSERT INTO subscription(uuid, user_id, checkout_session_id, created_by, updated_by)
                       VALUES (?, ?, ?)
                       """,
            (
                str(
                    uuid.uuid4(),
                ),
                user_id,
                checkout_session_id,
                user_id,
                user_id,
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

    def get_subscriptions_by_customer_id(
        self, cursor: sqlite3.Cursor, customer_id: str
    ):
        cursor.execute(
            "SELECT * FROM subscription WHERE customer_id = ?", (customer_id,)
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
        self,
        cursor: sqlite3.Cursor,
        id: int,
        current_user_id: Optional[int] = None,
        checkout_session_id: Optional[str] = None,
        customer_id: Optional[str] = None,
        status: Optional[bool] = None,
    ) -> int | None:
        query = "UPDATE subscription SET updated_at = ? "
        params = (str(datetime.now()),)

        if not checkout_session_id and status is None and not customer_id:
            raise Exception("Provide at least 1 update value.")

        if checkout_session_id:
            query += ", checkout_session_id = ? "
            params += (checkout_session_id,)
        if status is not None:
            query += ", status = ? "
            params += (status,)
        if customer_id:
            query += ", customer_id = ? "
            params += (customer_id,)
        if current_user_id:
            query += ", updated_by = ? "
            params += (current_user_id,)

        query += "WHERE id = ?"
        params += (id,)

        cursor.execute(query, params)
        return cursor.rowcount
