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