from psycopg2.extras import RealDictCursor
from modules.database.db import Database


class TeamRepository:

    def __init__(self):
        self.db = Database()

    def get_all(self):
        """
        Liefert alle Mannschaften.
        """

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    team_id,
                    name,
                    season_id,
                    active
                FROM teams
                ORDER BY name
                """
            )

            return cur.fetchall()

    def get_active(self):
        """
        Liefert nur aktive Mannschaften.
        """

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    team_id,
                    name,
                    season_id,
                    active
                FROM teams
                WHERE active = TRUE
                ORDER BY name
                """
            )

            return cur.fetchall()

    def count(self):
        """
        Anzahl der Mannschaften.
        """

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT COUNT(*) AS total
                FROM teams
                """
            )

            row = cur.fetchone()

        return row["total"]

    def save(self, name, season_id, active=True):
        """
        Legt eine Mannschaft an oder aktualisiert sie.
        Eindeutig ist die Kombination aus Name und Saison.
        """

        conn = self.db.connect()

        clean_name = name.strip()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT team_id
                    FROM teams
                    WHERE season_id = %s
                    AND LOWER(name) = LOWER(%s)
                    """,
                    (
                        season_id,
                        clean_name,
                    )
                )

                existing = cur.fetchone()

                if existing:
                    team_id = existing[0]

                    cur.execute(
                        """
                        UPDATE teams
                        SET
                            name = %s,
                            active = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE team_id = %s
                        """,
                        (
                            clean_name,
                            active,
                            team_id,
                        )
                    )

                else:
                    cur.execute(
                        """
                        INSERT INTO teams
                        (
                            season_id,
                            name,
                            active
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s
                        )
                        RETURNING team_id
                        """,
                        (
                            season_id,
                            clean_name,
                            active,
                        )
                    )

                    team_id = cur.fetchone()[0]

            conn.commit()
            return team_id

        except Exception:
            conn.rollback()
            raise

    def update(self, team_id, name, season_id, active=True):

        conn = self.db.connect()
        clean_name = name.strip()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE teams
                    SET
                        name = %s,
                        season_id = %s,
                        active = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE team_id = %s
                    """,
                    (
                        clean_name,
                        season_id,
                        active,
                        team_id,
                    )
                )

                if cur.rowcount == 0:
                    raise ValueError(
                        f"Mannschaft mit TEAM_ID {team_id} wurde nicht gefunden."
                    )

            conn.commit()

        except Exception:
            conn.rollback()
            raise


    def archive(self, team_id):

        conn = self.db.connect()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE teams
                    SET
                        active = FALSE,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE team_id = %s
                    """,
                    (team_id,)
                )

                if cur.rowcount == 0:
                    raise ValueError(
                        f"Mannschaft mit TEAM_ID {team_id} wurde nicht gefunden."
                    )

            conn.commit()

        except Exception:
            conn.rollback()
            raise
    
    def delete(self, team_id):

        conn = self.db.connect()

        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM teams
                WHERE team_id = %s
                """,
                (team_id,)
            )

        conn.commit()        