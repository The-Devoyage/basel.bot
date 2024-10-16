import sqlite3


class SkillModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_skill_by_id(self, cursor, skill_id):
        """Retrieve a skill by its ID using the provided cursor."""
        cursor.execute(
            """
            SELECT * FROM skill WHERE id = ?
        """,
            (skill_id,),
        )
        return cursor.fetchone()

    def get_skills(self, cursor):
        """Retrieve all skills using the provided cursor."""
        cursor.execute(
            """
            SELECT * FROM skill
        """
        )
        return cursor.fetchall()
