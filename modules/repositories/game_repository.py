from modules.database.db import Database

class GameRepository:

    def __init__(self):

        self.db = Database()


    def get_active_season(self):

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT season_id
            FROM seasons
            WHERE active = TRUE
            LIMIT 1
        """)

        row = cur.fetchone()

        return row[0] if row else None


    def get_team_id(self, season_id, team_name):

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT team_id
            FROM teams
            WHERE season_id=%s
              AND active=TRUE
              AND LOWER(name)=LOWER(%s)
            LIMIT 1
        """, (season_id, team_name))

        row = cur.fetchone()

        return row[0] if row else None

    def get_or_create_team(self, season_id, team_name):

        team_name = str(team_name).strip()

        team_id = self.get_team_id(
            season_id,
            team_name
        )

        if team_id is not None:
            return team_id

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO teams (
                season_id,
                name,
                active
            )
            VALUES (%s, %s, TRUE)
            RETURNING team_id
        """, (
            season_id,
            team_name
        ))

        team_id = cur.fetchone()[0]

        conn.commit()

        print(
            f"Team automatisch angelegt: "
            f"{team_name} – TEAM_ID {team_id}"
        )

        return team_id    


    def get_place_id(self, place_name):

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT place_id
            FROM places
            WHERE active=TRUE
              AND LOWER(name)=LOWER(%s)
            LIMIT 1
        """, (place_name,))

        row = cur.fetchone()

        return row[0] if row else None

    def exists_by_source_key(self, source_key):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 1
            FROM games
            WHERE source_key = %s
            LIMIT 1
        """, (source_key,))

        return cursor.fetchone() is not None   

    def insert_game(
        self,
        season_id,
        team_id,
        place_id,
        round_number,
        game_date,
        start_time,
        end_time,
        opponent,
        home_away,
        game_type,
        status,
        notes,
        source_file,
        source_sheet,
        source_row,
        source_key,
    ):
        cursor = self.db.connection.cursor()

        cursor.execute("""
            INSERT INTO games (
                season_id,
                team_id,
                place_id,
                round_number,
                game_date,
                start_time,
                end_time,
                opponent,
                home_away,
                game_type,
                status,
                notes,
                source_file,
                source_sheet,
                source_row,
                source_key
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s
            )
            RETURNING game_id;
        """, (
            season_id,
            team_id,
            place_id,
            round_number,
            game_date,
            start_time,
            end_time,
            opponent,
            home_away,
            game_type,
            status,
            notes,
            source_file,
            source_sheet,
            source_row,
            source_key,
        ))

        game_id = cursor.fetchone()[0]

        self.db.connection.commit()

        return game_id  

    def get_all_games(self):

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                g.game_id,
                g.game_date,
                g.start_time,
                g.end_time,
                t.name AS team_name,
                g.opponent,
                g.home_away,
                g.game_type,
                g.status,
                p.name AS place_name
            FROM games g

            INNER JOIN teams t
                ON t.team_id = g.team_id

            LEFT JOIN places p
                ON p.place_id = g.place_id

            ORDER BY
                g.game_date ASC,
                g.start_time ASC
        """)

        columns = [
            "game_id",
            "game_date",
            "start_time",
            "end_time",
            "team_name",
            "opponent",
            "home_away",
            "game_type",
            "status",
            "place_name",
        ]

        return [
            dict(zip(columns, row))
            for row in cur.fetchall()
        ]      