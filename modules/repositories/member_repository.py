import pandas as pd
from psycopg2.extras import RealDictCursor

from modules.database.db import Database


class MemberRepository:
    """
    Datenbankzugriff für Mitglieder.
    """

    def __init__(self):
        self.db = Database()

    def count(self):
        """
        Anzahl der Personen in der Datenbank.
        """
        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT COUNT(*) AS total
                FROM persons
                """
            )

            row = cur.fetchone()

        return row["total"]

    def get_all(self):
        """
        Liefert alle Mitglieder aus PostgreSQL.
        """

        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    person_id,
                    external_member_id,
                    first_name,
                    last_name,
                    birth_date
                FROM persons
                WHERE active = TRUE
                ORDER BY
                    last_name,
                    first_name
                """
            )

            return cur.fetchall()    

    def get_by_id(self, person_id):
        """
        Lädt eine Person vollständig anhand der person_id.
        """

        conn = self.db.connect()

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT
                    person_id AS "PERSON_ID",
                    external_member_id AS "MEMBER_ID",
                    first_name AS "VORNAME",
                    last_name AS "NACHNAME",
                    birth_date AS "GEBURTSDATUM",
                    gender AS "GESCHLECHT",
                    mobile AS "MOBIL",
                    email AS "EMAIL",
                    player_pass_number AS "SPIELERPASSNUMMER",
                    entry_date AS "EINTRITT",
                    exit_date AS "AUSTRITT",
                    status AS "STATUS",
                    note AS "BEMERKUNG",
                    active AS "AKTIV"
                FROM persons
                WHERE person_id = %s
                """,
                (person_id,)
            )

            row = cur.fetchone()

        if row is None:
            return None

        return dict(row)        
            

    def exists(self, external_member_id):
        """
        Prüft, ob ein Mitglied bereits importiert wurde.
        """
        conn = self.db.connect()

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT 1
                FROM persons
                WHERE external_member_id = %s
                """,
                (str(external_member_id),)
            )

            return cur.fetchone() is not None

    def save(self, member):
        """
        Legt ein Mitglied an oder aktualisiert es.
        """

        conn = self.db.connect()

        person_id = member.get("person_id")
        external_member_id = member.get("external_member_id")

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            if not person_id and external_member_id is None:
                cur.execute(
                    """
                    SELECT COALESCE(MAX(external_member_id), 0) + 1 AS next_id
                    FROM persons
                    """
                )

                external_member_id = cur.fetchone()["next_id"]    

            if person_id:
                cur.execute(
                    """
                    UPDATE persons
                    SET
                        external_member_id = %s,
                        first_name = %s,
                        last_name = %s,
                        birth_date = %s,
                        gender = %s,
                        mobile = %s,
                        email = %s,
                        player_pass_number = %s,
                        entry_date = %s,
                        exit_date = %s,
                        status = %s,
                        note = %s,
                        active = %s,
                        updated_at = NOW()
                    WHERE person_id = %s
                    RETURNING person_id
                    """,
                    (
                        external_member_id,
                        member.get("first_name"),
                        member.get("last_name"),
                        member.get("birth_date"),
                        member.get("gender"),
                        member.get("mobile"),
                        member.get("email"),
                        member.get("player_pass_number"),
                        member.get("entry_date"),
                        member.get("exit_date"),
                        member.get("status", "Aktiv"),
                        member.get("note"),
                        member.get("active", True),
                        person_id,
                    )
                )

            else:
                cur.execute(
                    """
                    INSERT INTO persons
                    (
                        external_member_id,
                        first_name,
                        last_name,
                        birth_date,
                        gender,
                        mobile,
                        email,
                        player_pass_number,
                        entry_date,
                        exit_date,
                        status,
                        note,
                        active
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s
                    )
                    RETURNING person_id
                    """,
                    (
                        external_member_id,
                        member.get("first_name"),
                        member.get("last_name"),
                        member.get("birth_date"),
                        member.get("gender"),
                        member.get("mobile"),
                        member.get("email"),
                        member.get("player_pass_number"),
                        member.get("entry_date"),
                        member.get("exit_date"),
                        member.get("status", "Aktiv"),
                        member.get("note"),
                        member.get("active", True),
                    )
                )

            result = cur.fetchone()

        conn.commit()

        return result["person_id"]

    def save_many(self, members):
        """
        Importiert mehrere Mitglieder in einer gemeinsamen Transaktion.

        Existierende Mitglieder werden aktualisiert.
        Neue Mitglieder werden angelegt.
        Geänderte Mitgliedsnummern werden über Name und Geburtstag erkannt.
        """

        conn = self.db.connect()

        inserted = 0
        updated = 0
        reassigned = 0

        try:
            with conn.cursor() as cur:
                for member in members:
                    external_member_id = int(member["ID"])

                    first_name = member["Vorname"]
                    last_name = member["Nachname"]

                    birth_date = member["Geburtstag"]
                    if pd.isna(birth_date):
                        birth_date = None

                    # 1. Mitglied über die externe ID suchen
                    cur.execute(
                        """
                        SELECT person_id
                        FROM persons
                        WHERE external_member_id = %s
                        """,
                        (external_member_id,)
                    )

                    existing_by_id = cur.fetchone()

                    if existing_by_id:
                        cur.execute(
                            """
                            UPDATE persons
                            SET
                                first_name = %s,
                                last_name = %s,
                                birth_date = %s
                            WHERE person_id = %s
                            """,
                            (
                                first_name,
                                last_name,
                                birth_date,
                                existing_by_id[0],
                            )
                        )

                        updated += 1
                        continue

                    # 2. Dieselbe Person eventuell unter einer alten ID suchen
                    cur.execute(
                        """
                        SELECT person_id
                        FROM persons
                        WHERE first_name = %s
                        AND last_name = %s
                        AND birth_date IS NOT DISTINCT FROM %s
                        """,
                        (
                            first_name,
                            last_name,
                            birth_date,
                        )
                    )

                    existing_by_identity = cur.fetchone()

                    if existing_by_identity:
                        cur.execute(
                            """
                            UPDATE persons
                            SET
                                external_member_id = %s,
                                first_name = %s,
                                last_name = %s,
                                birth_date = %s
                            WHERE person_id = %s
                            """,
                            (
                                external_member_id,
                                first_name,
                                last_name,
                                birth_date,
                                existing_by_identity[0],
                            )
                        )

                        reassigned += 1
                        continue

                    # 3. Neue Person anlegen
                    cur.execute(
                        """
                        INSERT INTO persons
                        (
                            external_member_id,
                            first_name,
                            last_name,
                            birth_date
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s,
                            %s
                        )
                        """,
                        (
                            external_member_id,
                            first_name,
                            last_name,
                            birth_date,
                        )
                    )

                    inserted += 1

            conn.commit()

        except Exception:
            conn.rollback()
            raise

        return {
            "inserted": inserted,
            "updated": updated,
            "reassigned": reassigned,
        }   

    def archive(self, person_id):

        conn = self.db.connect()

        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE persons
                SET
                    active = FALSE,
                    status = 'Archiviert',
                    updated_at = NOW()
                WHERE person_id = %s
                """,
                (person_id,)
            )

        conn.commit()     