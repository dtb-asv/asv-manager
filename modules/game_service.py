"""
=========================================================
ASV Manager
Game Service
=========================================================
Zentrale Verwaltung aller Spiele.
"""

from modules.excel_reader import ExcelReader
from modules.excel_writer import ExcelWriter


class GameService:

    def __init__(self):

        self.reader = ExcelReader()
        self.writer = ExcelWriter()

    # -------------------------------------------------

    def load_games(self, excel_datei):

        self.reader.load(excel_datei)

        return self.reader.df.copy()

    # -------------------------------------------------

    def update_game(
        self,
        excel_datei,
        excel_zeile,
        daten
    ):

        self.writer.update_game(
            excel_datei,
            excel_zeile,
            daten
        )

    # -------------------------------------------------

    def add_game(
        self,
        excel_datei,
        daten
    ):

        self.writer.add_game(
            excel_datei,
            daten
        )

        # -------------------------------------------------

    def archive_game(
        self,
        excel_datei,
        excel_zeile,
        grund,
        bemerkung
    ):

        print(
            f"ARCHIVIEREN -> "
            f"Zeile={excel_zeile}, "
            f"Grund={grund}, "
            f"Bemerkung={bemerkung}"
        )    