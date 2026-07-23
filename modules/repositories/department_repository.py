from psycopg2.extras import RealDictCursor
from modules.database.db import Database


class DepartmentRepository:

    def __init__(self):
        self.db = Database()

    def get_all(self):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    department_id,
                    name,
                    active
                FROM departments
                ORDER BY name
                """
            )

            return cur.fetchall()

    def get_active(self):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    department_id,
                    name,
                    active
                FROM departments
                WHERE active = TRUE
                ORDER BY name
                """
            )

            return cur.fetchall()

    def get_by_id(self, department_id):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                SELECT
                    department_id,
                    name,
                    active
                FROM departments
                WHERE department_id = %s
                """,
                (department_id,)
            )

            return cur.fetchone()


    def save(self, department):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            if department.get("department_id"):

                cur.execute(
                    """
                    UPDATE departments
                    SET
                        name = %s,
                        active = %s,
                        updated_at = NOW()
                    WHERE department_id = %s
                    RETURNING department_id
                    """,
                    (
                        department["name"],
                        department.get("active", True),
                        department["department_id"]
                    )
                )

            else:

                cur.execute(
                    """
                    INSERT INTO departments
                    (
                        name,
                        active
                    )
                    VALUES
                    (
                        %s,
                        %s
                    )
                    RETURNING department_id
                    """,
                    (
                        department["name"],
                        department.get("active", True)
                    )
                )

            row = cur.fetchone()

        conn.commit()

        return row["department_id"]


    def archive(self, department_id):

        conn = self.db.connect()

        with conn.cursor() as cur:

            cur.execute(
                """
                UPDATE departments
                SET
                    active = FALSE,
                    updated_at = NOW()
                WHERE department_id = %s
                """,
                (department_id,)
            )

        conn.commit()        