import os

import pandas as pd

from modules.excel_reader import ExcelReader
from modules.repositories.game_repository import GameRepository


class GameImportService:

    def __init__(self):
        self.repository = GameRepository()
        self.reader = ExcelReader()

    @staticmethod
    def clean_value(value, default=None):
        if pd.isna(value):
            return default

        if isinstance(value, str):
            value = value.strip()
            return value if value else default

        return value

    @staticmethod
    def normalize_home_away(value):
        value = str(value or "").strip().lower()

        if value == "heim":
            return "Heim"

        if value in ("auswärts", "auswaerts"):
            return "Auswärts"

        return "Neutral"

    def import_excel(self, excel_file):

        print("Starte Spielimport...")

        season_id = self.repository.get_active_season()

        if season_id is None:
            raise RuntimeError("Keine aktive Saison gefunden.")

        self.reader.load(excel_file, sheet="ICS2")

        spiele = self.reader.games
        
        spiele = spiele[
            spiele["ART"]
            .astype(str)
            .str.strip()
            .str.lower()
            == "spiel"
        ].copy()

        print(spiele.columns.tolist())

        if spiele is None or spiele.empty:
            print("Im Tabellenblatt ICS2 wurden keine Spiele gefunden.")
            return {
                "imported": 0,
                "skipped": 0,
                "errors": 0,
            }

        print(f"{len(spiele)} Spiele gefunden.")

        imported = 0
        skipped = 0
        errors = 0

        for index, spiel in spiele.iterrows():

            excel_row = index + 2

            try:
                team_name = self.clean_value(spiel.get("LIGA"))

                if not team_name:
                    print(f"Zeile {excel_row}: LIGA fehlt.")
                    errors += 1
                    continue

                team_id = self.repository.get_or_create_team(
                    season_id,
                    team_name
                )

                place_name = self.clean_value(spiel.get("ORT"))
                place_id = None

                if place_name:
                    place_id = self.repository.get_place_id(place_name)

                game_date = self.clean_value(spiel.get("DATUM"))
                start_time = self.clean_value(spiel.get("STARTZEIT"))
                end_time = self.clean_value(spiel.get("ENDZEIT"))
                opponent = self.clean_value(
                    spiel.get("GEGNER"),
                    "Unbekannter Gegner"
                )

                if game_date is None:
                    print(f"Zeile {excel_row}: DATUM fehlt.")
                    errors += 1
                    continue

                home_away = self.normalize_home_away(
                    self.clean_value(spiel.get("TYP"))
                )

                game_type = self.clean_value(
                    spiel.get("ART"),
                    "Meisterschaft"
                )

                status = self.clean_value(
                    spiel.get("STATUS"),
                    "Aktiv"
                )

                notes = self.clean_value(
                    spiel.get("BESCHREIBUNG"),
                    ""
                )

                source_key = (
                    f"{season_id}|"
                    f"{team_name}|"
                    f"{game_date}|"
                    f"{start_time}|"
                    f"{opponent}"
                )

                if self.repository.exists_by_source_key(source_key):
                    print(
                        f"Zeile {excel_row}: "
                        f"{team_name} gegen {opponent} "
                        f"bereits vorhanden."
                    )
                    skipped += 1
                    continue

                game_id = self.repository.insert_game(
                    season_id=season_id,
                    team_id=team_id,
                    place_id=place_id,
                    round_number=None,
                    game_date=game_date,
                    start_time=start_time,
                    end_time=end_time,
                    opponent=opponent,
                    home_away=home_away,
                    game_type=game_type,
                    status=status,
                    notes=notes,
                    source_file=os.path.basename(excel_file),
                    source_sheet="ICS2",
                    source_row=excel_row,
                    source_key=source_key,
                )

                print(
                    f"Zeile {excel_row}: "
                    f"{team_name} gegen {opponent} "
                    f"importiert – GAME_ID {game_id}"
                )

                imported += 1

            except Exception as ex:
                print(f"Zeile {excel_row}: Fehler: {ex}")
                errors += 1

        print("--------------------------------")
        print(f"Importiert   : {imported}")
        print(f"Übersprungen: {skipped}")
        print(f"Fehler       : {errors}")

        return {
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
        }