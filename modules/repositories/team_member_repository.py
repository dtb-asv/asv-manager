from psycopg2.extras import RealDictCursor

from modules.database.db import Database


class TeamMemberRepository:

    def __init__(self):
        self.db = Database()

    def get_all_players(self):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                '''
                SELECT
                    p.person_id AS "MEMBER_ID",
                    p.first_name AS "VORNAME",
                    p.last_name AS "NACHNAME"
                FROM persons p
                WHERE p.active = TRUE
                  AND (
                        p.status IS NULL
                        OR LOWER(TRIM(p.status)) <> 'archiviert'
                      )
                ORDER BY
                    p.last_name,
                    p.first_name
                '''
            )

            return cur.fetchall()

    def get_team_players(self, team_id):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                '''
                SELECT
                    tm.team_member_id AS "TEAM_MEMBER_ID",
                    tm.team_id AS "TEAM_ID",
                    tm.person_id AS "MEMBER_ID",
                    tm.role AS "ROLLE",
                    p.first_name AS "VORNAME",
                    p.last_name AS "NACHNAME"
                FROM team_members tm
                INNER JOIN persons p
                    ON p.person_id = tm.person_id
                WHERE tm.team_id = %s
                  AND LOWER(TRIM(tm.role)) = 'spieler'
                  AND tm.valid_until IS NULL
                  AND p.active = TRUE
                ORDER BY
                    p.last_name,
                    p.first_name
                ''',
                (team_id,)
            )

            return cur.fetchall()

    def assign_player(self, team_id, person_id):

        conn = self.db.connect()

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:

                cur.execute(
                    '''
                    SELECT team_member_id
                    FROM team_members
                    WHERE team_id = %s
                      AND person_id = %s
                      AND LOWER(TRIM(role)) = 'spieler'
                      AND valid_until IS NULL
                    ''',
                    (team_id, person_id)
                )

                existing = cur.fetchone()

                if existing:
                    return False

                cur.execute(
                    '''
                    INSERT INTO team_members (
                        team_id,
                        person_id,
                        role,
                        valid_from,
                        valid_until
                    )
                    VALUES (
                        %s,
                        %s,
                        'Spieler',
                        CURRENT_DATE,
                        NULL
                    )
                    ON CONFLICT (team_id, person_id, role)
                    DO UPDATE SET
                        valid_from = CURRENT_DATE,
                        valid_until = NULL
                    RETURNING team_member_id
                    ''',
                    (team_id, person_id)
                )

                result = cur.fetchone()

            conn.commit()

            return result is not None

        except Exception:
            if conn is not None and conn.closed == 0:
                conn.rollback()
            raise

    def remove_player(self, team_member_id):

        conn = self.db.connect()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    '''
                    UPDATE team_members
                    SET valid_until = CURRENT_DATE
                    WHERE team_member_id = %s
                      AND valid_until IS NULL
                    ''',
                    (team_member_id,)
                )

                success = cur.rowcount > 0

            conn.commit()

            return success

        except Exception:
            if conn is not None and conn.closed == 0:
                conn.rollback()
            raise

    def get_team_staff(self, team_id):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                SELECT
                    tm.team_member_id AS "TEAM_MEMBER_ID",
                    tm.team_id AS "TEAM_ID",
                    tm.person_id AS "MEMBER_ID",
                    tm.role AS "ROLLE",
                    p.first_name AS "VORNAME",
                    p.last_name AS "NACHNAME"
                FROM team_members tm
                INNER JOIN persons p
                    ON p.person_id = tm.person_id
                WHERE tm.team_id = %s
                AND LOWER(TRIM(tm.role)) = 'trainer'
                AND tm.valid_until IS NULL
                AND p.active = TRUE
                ORDER BY
                    p.last_name,
                    p.first_name
                """,
                (team_id,)
            )

            return cur.fetchall()

    def get_all_staff(self):

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                SELECT
                    person_id AS "MEMBER_ID",
                    first_name AS "VORNAME",
                    last_name AS "NACHNAME"
                FROM persons
                WHERE active = TRUE
                AND (
                        status IS NULL
                        OR LOWER(TRIM(status)) <> 'archiviert'
                    )
                ORDER BY
                    last_name,
                    first_name
                """
            )

            return cur.fetchall()                

    def assign_staff(self, team_id, person_id):

        conn = self.db.connect()

        try:

            with conn.cursor(cursor_factory=RealDictCursor) as cur:

                cur.execute(
                    """
                    SELECT team_member_id
                    FROM team_members
                    WHERE team_id=%s
                    AND person_id=%s
                    AND LOWER(TRIM(role))='trainer'
                    AND valid_until IS NULL
                    """,
                    (team_id, person_id)
                )

                if cur.fetchone():
                    return False

                cur.execute(
                    """
                    INSERT INTO team_members
                    (
                        team_id,
                        person_id,
                        role,
                        valid_from,
                        valid_until
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        'Trainer',
                        CURRENT_DATE,
                        NULL
                    )
                    RETURNING team_member_id
                    """,
                    (team_id, person_id)
                )

                result = cur.fetchone()

            conn.commit()

            return result is not None

        except Exception:

            if conn.closed == 0:
                conn.rollback()

            raise

    def remove_staff(self, team_member_id):

        conn = self.db.connect()

        try:

            with conn.cursor() as cur:

                cur.execute(
                    """
                    UPDATE team_members
                    SET valid_until=CURRENT_DATE
                    WHERE team_member_id=%s
                    AND valid_until IS NULL
                    """,
                    (team_member_id,)
                )

                success = cur.rowcount > 0

            conn.commit()

            return success

        except Exception:

            if conn.closed == 0:
                conn.rollback()

            raise                
