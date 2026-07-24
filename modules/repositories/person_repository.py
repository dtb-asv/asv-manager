from psycopg2.extras import RealDictCursor
from modules.database.db import Database


class PersonRepository:

    def __init__(self):
        self.db = Database()

    def get_all(self):

        conn = self.db.connect()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT
                        person_id,
                        external_member_id,
                        first_name,
                        last_name,
                        birth_date,
                        active,
                        gender,
                        mobile,
                        email,
                        player_pass_number,
                        entry_date,
                        exit_date,
                        status,
                        note
                    FROM persons
                    ORDER BY
                        last_name,
                        first_name
                    """
                )

                return cur.fetchall()

        except Exception:
            conn.rollback()
            raise


    def get_by_id(self, person_id):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    person_id,
                    external_member_id,
                    first_name,
                    last_name,
                    birth_date,
                    active,
                    gender,
                    mobile,
                    email,
                    player_pass_number,
                    entry_date,
                    exit_date,
                    status,
                    note
                FROM persons
                WHERE person_id = %s
                """,
                (person_id,)
            )

            return cur.fetchone()



    def update(
        self,
        person_id,
        first_name,
        last_name,
        birth_date,
        mobile,
        email,
        status,
        active,
        note
    ):
        conn = self.db.connect()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE persons
                    SET
                        first_name = %s,
                        last_name = %s,
                        birth_date = %s,
                        mobile = %s,
                        email = %s,
                        status = %s,
                        active = %s,
                        note = %s
                    WHERE person_id = %s
                    """,
                    (
                        first_name,
                        last_name,
                        birth_date,
                        mobile,
                        email,
                        status,
                        active,
                        note,
                        person_id
                    )
                )

            conn.commit()

        except Exception:
            conn.rollback()
            raise
