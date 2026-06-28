from datetime import datetime
from openpyxl import load_workbook
import pandas as pd

from modules.constants import SHEET_MEMBERS
from modules.member_writer import MemberWriter


class MemberService:

    def __init__(self):
        self.writer = MemberWriter()

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

        self.writer.add_member(excel_datei, daten)