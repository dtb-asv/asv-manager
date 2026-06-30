import pandas as pd

from datetime import datetime
from openpyxl import load_workbook
from modules.constants import SHEET_MEMBERS
from modules.member_writer import MemberWriter
from modules.history_service import HistoryService


class MemberService:

    def __init__(self):
        self.writer = MemberWriter()
        self.history = HistoryService()

    def load_members(self, excel_datei):
        wb = load_workbook(excel_datei)

        if SHEET_MEMBERS not in wb.sheetnames:
            ws = wb.create_sheet(SHEET_MEMBERS)
            ws.append([
                "MEMBER_ID",
                "VORNAME",
                "NACHNAME",
                "GEBURTSDATUM",
                "EINTRITT",
                "AUSTRITT",
                "STATUS",
                "BEMERKUNG"
            ])
            wb.save(excel_datei)

        return pd.read_excel(
            excel_datei,
            sheet_name=SHEET_MEMBERS
        )

    def next_member_id(self, excel_datei):
        df = self.load_members(excel_datei)

        if df.empty or "MEMBER_ID" not in df.columns:
            return "MEMBER000001"

        nummern = []

        for value in df["MEMBER_ID"].dropna():
            text = str(value)
            if text.startswith("MEMBER"):
                nummern.append(int(text.replace("MEMBER", "")))

        next_number = max(nummern, default=0) + 1
        return f"MEMBER{next_number:06d}"

    def add_member(self, excel_datei, daten):
        daten["MEMBER_ID"] = self.next_member_id(excel_datei)
        daten["EINTRITT"] = datetime.now().strftime("%d.%m.%Y")
        daten["STATUS"] = "Aktiv"

        member_id = self.writer.add_member(excel_datei, daten)
        return member_id

    def update_member(self, excel_datei, member_id, daten):

        grund = daten.pop("_GRUND", "")
        bemerkung = daten.pop("_BEMERKUNG", "")

        self.writer.update_member(
            excel_datei,
            member_id,
            daten
        )

        objekt = (
            f"{daten.get('VORNAME', '')} "
            f"{daten.get('NACHNAME', '')}"
        ).strip()

        self.history.log(
            excel_datei=excel_datei,
            bereich="Mitglied",
            aktion="Bearbeitet",
            objekt=objekt,
            excel_zeile="",
            game_id=member_id,
            grund=grund,
            bemerkung=bemerkung,
            benutzer="System"
        )

    def archive_member(self, excel_datei, member_id):

        self.writer.archive_member(
            excel_datei,
            member_id
        )

        self.history.log(
            excel_datei=excel_datei,
            bereich="Mitglied",
            aktion="Archiviert",
            objekt=member_id,
            excel_zeile="",
            game_id=member_id,
            grund="",
            bemerkung="Mitglied wurde archiviert",
            benutzer="System"
        )