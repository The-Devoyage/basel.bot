import sqlite3
import uuid
from datetime import datetime
from typing import Optional
import logging

from classes.user import User


logger = logging.getLogger(__name__)


class UserModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_user(
        self,
        cursor,
        email,
    ) -> int:
        """Create a new user with a generated UUID."""
        user_uuid = str(uuid.uuid4())
        auth_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO user (uuid, email, auth_id, role_id )
            VALUES (
                ?, ?, ?,
                (SELECT id FROM role WHERE identifier = 'user')
            )
        """,
            (
                user_uuid,
                email,
                auth_id,
            ),
        )
        return cursor.lastrowid  # Return the newly created user's ID

    def get_user_by_id(self, cursor, user_id) -> Optional[User]:
        """Retrieve a user by their ID."""
        cursor.execute(
            """
            SELECT * FROM user WHERE id = ?
        """,
            (user_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))

        try:
            return User(**data)
        except Exception as e:
            logger.error(f"Failed to create user object: {e}")
            raise

    def get_user_by_uuid(self, cursor, user_uuid) -> Optional[User]:
        """Retrieve a user by their UUID."""
        cursor.execute(
            """
            SELECT * FROM user WHERE uuid = ?
        """,
            (user_uuid,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))

        try:
            return User(**data)
        except Exception as e:
            logger.error(f"Failed to create user object: {e}")
            raise

    def get_user_by_email(self, cursor, email) -> Optional[User]:
        """Retrieve a user by their email."""
        cursor.execute(
            """
            SELECT * FROM user WHERE email = ?
        """,
            (email,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))

        try:
            return User(**data)
        except Exception as e:
            logger.error(f"Failed to create user object: {e}")
            raise

    def get_user_by_auth_id(self, cursor, auth_id) -> Optional[User]:
        """Retrieve a user by their auth ID."""
        cursor.execute(
            """
            SELECT * FROM user WHERE auth_id = ?
        """,
            (auth_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, row))

        try:
            return User(**data)
        except Exception as e:
            logger.error(f"Failed to create user object: {e}")
            raise

    def update_user(
        self,
        cursor,
        user_id: int,
        current_user: User,
        email=None,
        first_name=None,
        last_name=None,
        phone=None,
        role_id=None,
        status=None,
        image=None,
        auth_id=None,
    ) -> int:
        """Update a user's information."""
        logger.debug(f"Updating user {user_id}")

        query = """
            UPDATE user
            SET updated_by = ?, updated_at = ?
        """

        bindings = (current_user.id, datetime.now())

        if email is not None:
            query += ", email = ?"
            bindings += (email,)
        if first_name is not None:
            query += ", first_name = ?"
            bindings += (first_name,)
        if last_name is not None:
            query += ", last_name = ?"
            bindings += (last_name,)
        if phone is not None:
            query += ", phone = ?"
            bindings += (phone,)
        if role_id is not None:
            query += ", role_id = ?"
            bindings += (role_id,)
        if status is not None:
            query += ", status = ?"
            bindings += (status,)
        if image is not None:
            query += ", image = ?"
            bindings += (image,)
        if auth_id is not None:
            query += ", auth_id = ?"
            bindings += (auth_id,)

        query += " WHERE id = ?"

        cursor.execute(
            query,
            bindings + (user_id,),
        )

        return cursor.rowcount  # Return the number of rows updated

    def delete_user(self, cursor, user_id, deleted_by) -> int:
        """Soft delete a user."""
        cursor.execute(
            """
            UPDATE user
            SET deleted_by = ?, deleted_at = ?
            WHERE id = ?
        """,
            (deleted_by, datetime.now(), user_id),
        )
        return cursor.rowcount  # Return the number of rows updated (soft delete)
