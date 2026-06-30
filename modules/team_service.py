from openpyxl import load_workbook
from modules.team_writer import TeamWriter
from modules.history_service import HistoryService
import pandas as pd

from modules.constants import (
    SHEET_TEAMS,
    SHEET_TEAM_VEREINE,
    SHEET_TEAM_TRAINER
)


class TeamService:

    def __init__(self):

        self.writer = TeamWriter() 
        self.history = HistoryService()

    def ensure_sheets(self, excel_datei):

        wb = load_workbook(excel_datei)

        if SHEET_TEAMS not in wb.sheetnames:
            ws = wb.create_sheet(SHEET_TEAMS)
            ws.append([
                "TEAM_ID",
                "SAISON",
                "MANNSCHAFT",
                "TYP",
                "AKTIV",
                "LEADVEREIN",
                "BEMERKUNG"
            ])

        if SHEET_TEAM_VEREINE not in wb.sheetnames:
            ws = wb.create_sheet(SHEET_TEAM_VEREINE)
            ws.append([
                "TEAM_ID",
                "VEREIN",
                "ROLLE"
            ])

        if SHEET_TEAM_TRAINER not in wb.sheetnames:
            ws = wb.create_sheet(SHEET_TEAM_TRAINER)
            ws.append([
                "TEAM_ID",
                "MEMBER_ID",
                "ROLLE"
            ])

        wb.save(excel_datei)

       

    def load_teams(self, excel_datei):

        self.ensure_sheets(excel_datei)

        return pd.read_excel(
            excel_datei,
            sheet_name=SHEET_TEAMS
        )

    def next_team_id(self, excel_datei):

        df = self.load_teams(excel_datei)

        if df.empty or "TEAM_ID" not in df.columns:
            return "TEAM000001"

        nummern = []

        for value in df["TEAM_ID"].dropna():

            text = str(value)

            if text.startswith("TEAM"):

                try:
                    nummern.append(
                        int(text.replace("TEAM", ""))
                    )
                except ValueError:
                    pass

        next_number = max(nummern, default=0) + 1

        return f"TEAM{next_number:06d}"

    def add_team(self, excel_datei, daten):

        daten["TEAM_ID"] = self.next_team_id(excel_datei)
        daten["AKTIV"] = "Ja"

        self.writer.add_team(
            excel_datei,
            daten
        )   

    def update_team(self, excel_datei, team_id, daten):

        grund = daten.pop("_GRUND", "")
        bemerkung = daten.pop("_BEMERKUNG", "")

        self.writer.update_team(
            excel_datei,
            team_id,
            daten
        )

        objekt = daten.get("MANNSCHAFT", team_id)

        self.history.log(
            excel_datei=excel_datei,
            bereich="Mannschaft",
            aktion="Bearbeitet",
            objekt=objekt,
            excel_zeile="",
            game_id=team_id,
            grund=grund,
            bemerkung=bemerkung,
            benutzer="System"
        )

    def archive_team(self, excel_datei, team_id):

        self.writer.archive_team(
            excel_datei,
            team_id
        )

        self.history.log(
            excel_datei=excel_datei,
            bereich="Mannschaft",
            aktion="Archiviert",
            objekt=team_id,
            excel_zeile="",
            game_id=team_id,
            grund="",
            bemerkung="Mannschaft wurde archiviert",
            benutzer="System"
        )

    