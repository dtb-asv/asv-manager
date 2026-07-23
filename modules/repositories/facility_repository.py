from psycopg2.extras import RealDictCursor

from modules.database.db import Database


class FacilityRepository:

    def __init__(self):
        self.db = Database()

    def get_all(self):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    facility_id,
                    name,
                    address,
                    active,
                    created_at,
                    updated_at
                FROM facilities
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
                    facility_id,
                    name,
                    address,
                    active,
                    created_at,
                    updated_at
                FROM facilities
                WHERE active = TRUE
                ORDER BY name
                """
            )

            return cur.fetchall()

    def get_by_id(self, facility_id):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    facility_id,
                    name,
                    address,
                    active,
                    created_at,
                    updated_at
                FROM facilities
                WHERE facility_id = %s
                """,
                (facility_id,)
            )

            return cur.fetchone()

    def save(self, facility):

        conn = self.db.connect()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:

                if facility.get("facility_id"):

                    cur.execute(
                        """
                        UPDATE facilities
                        SET
                            name = %s,
                            address = %s,
                            active = %s,
                            updated_at = NOW()
                        WHERE facility_id = %s
                        RETURNING facility_id
                        """,
                        (
                            facility["name"],
                            facility.get("address", ""),
                            facility.get("active", True),
                            facility["facility_id"]
                        )
                    )

                else:

                    cur.execute(
                        """
                        INSERT INTO facilities
                        (
                            name,
                            address,
                            active,
                            created_at,
                            updated_at
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s,
                            NOW(),
                            NOW()
                        )
                        RETURNING facility_id
                        """,
                        (
                            facility["name"],
                            facility.get("address", ""),
                            facility.get("active", True)
                        )
                    )

                row = cur.fetchone()

            conn.commit()

            return row["facility_id"]

        except Exception:
            conn.rollback()
            raise

    def archive(self, facility_id):

        conn = self.db.connect()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE facilities
                    SET
                        active = FALSE,
                        updated_at = NOW()
                    WHERE facility_id = %s
                    """,
                    (facility_id,)
                )

            conn.commit()

        except Exception:
            conn.rollback()
            raise