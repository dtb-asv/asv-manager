from psycopg2.extras import RealDictCursor

from modules.database.db import Database


class PlaceRepository:

    def __init__(self):
        self.db = Database()

    def get_all(self):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    p.place_id,
                    p.facility_id,
                    p.name,
                    p.address,
                    p.training_zones,
                    p.active,
                    f.name AS facility_name
                FROM places p
                LEFT JOIN facilities f
                    ON f.facility_id = p.facility_id
                ORDER BY p.name
                """
            )

            return cur.fetchall()

    def get_active(self):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    p.place_id,
                    p.facility_id,
                    p.name,
                    p.address,
                    p.training_zones,
                    p.active,
                    f.name AS facility_name
                FROM places p
                LEFT JOIN facilities f
                    ON f.facility_id = p.facility_id
                WHERE p.active = TRUE
                ORDER BY p.name
                """
            )

            return cur.fetchall()

    def get_by_id(self, place_id):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    place_id,
                    facility_id,
                    name,
                    address,
                    training_zones,
                    active
                FROM places
                WHERE place_id = %s
                """,
                (place_id,)
            )

            return cur.fetchone()

    def save(self, place):

        conn = self.db.connect()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:

                if place.get("place_id"):

                    cur.execute(
                        """
                        UPDATE places
                        SET
                            facility_id = %s,
                            name = %s,
                            address = %s,
                            training_zones = %s,
                            active = %s,
                            updated_at = NOW()
                        WHERE place_id = %s
                        RETURNING place_id
                        """,
                        (
                            place.get("facility_id"),
                            place["name"],
                            place.get("address"),
                            place.get("training_zones"),
                            place.get("active", True),
                            place["place_id"]
                        )
                    )

                else:

                    cur.execute(
                        """
                        INSERT INTO places
                        (
                            facility_id,
                            name,
                            address,
                            training_zones,
                            active
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        )
                        RETURNING place_id
                        """,
                        (
                            place.get("facility_id"),
                            place["name"],
                            place.get("address"),
                            place.get("training_zones"),
                            place.get("active", True)
                        )
                    )

                row = cur.fetchone()

            conn.commit()

            return row["place_id"]

        except Exception:
            conn.rollback()
            raise

    def archive(self, place_id):

        conn = self.db.connect()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE places
                    SET
                        active = FALSE,
                        updated_at = NOW()
                    WHERE place_id = %s
                    """,
                    (place_id,)
                )

            conn.commit()

        except Exception:
            conn.rollback()
            raise