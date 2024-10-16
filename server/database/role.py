import sqlite3


class RoleModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_role_by_id(self, cursor, role_id):
        """Retrieve a role by its ID using the provided cursor."""
        cursor.execute(
            """
            SELECT * FROM role WHERE id = ?
            """,
            (role_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))

    def get_role_by_identifier(self, cursor, identifier):
        """Retrieve a role by its identifier using the provided cursor."""
        cursor.execute(
            """
            SELECT * FROM role WHERE identifier = ?
            """,
            (identifier,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))

    def get_roles(self, cursor):
        """Retrieve all roles using the provided cursor."""
        cursor.execute(
            """
            SELECT * FROM role
            """
        )
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
