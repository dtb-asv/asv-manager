from psycopg2.extras import RealDictCursor
from modules.database.db import Database


class SeasonRepository:

    def __init__(self):
        self.db = Database()

    def get_all(self):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    season_id,
                    name,
                    active
                FROM seasons
                ORDER BY season_id
                """
            )

            return cur.fetchall()

    def get_active(self):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    season_id,
                    name,
                    active
                FROM seasons
                WHERE active = TRUE
                ORDER BY season_id
                """
            )

            return cur.fetchall()


    def get_by_id(self, season_id):
        """
        Lädt eine einzelne Saison anhand ihrer ID.
        """

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    season_id,
                    name,
                    active
                FROM seasons
                WHERE season_id = %s
                """,
                (season_id,)
            )

            return cur.fetchone()

    def save(self, name, active=True):
        """
        Legt eine neue Saison an.
        """

        conn = self.db.connect()
        clean_name = name.strip()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO seasons
                    (
                        name,
                        active
                    )
                    VALUES
                    (
                        %s,
                        %s
                    )
                    RETURNING season_id
                    """,
                    (
                        clean_name,
                        active,
                    )
                )

                season_id = cur.fetchone()[0]

            conn.commit()
            return season_id

        except Exception:
            conn.rollback()
            raise



    def update(self, season_id, name, active=True):
        conn = self.db.connect()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE seasons
                    SET
                        name = %s,
                        active = %s
                    WHERE season_id = %s
                    """,
                    (name.strip(), active, season_id)
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
