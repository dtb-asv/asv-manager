import pandas as pd

from modules.constants import SHEET_CLUB
from modules.club_writer import ClubWriter


class ClubService:

    def __init__(self):

        self.writer = ClubWriter()

    def load_club(self, excel_datei):

        df = pd.read_excel(
            excel_datei,
            sheet_name=SHEET_CLUB
        )

        if df.empty:
            return None

        return df.iloc[0].to_dict()

    def save_club(self, excel_datei, daten):

        if not daten.get("CLUB_ID"):
            daten["CLUB_ID"] = "CLUB000001"

        daten["AKTIV"] = "Ja"

        self.writer.save_club(
            excel_datei,
            daten
        )    