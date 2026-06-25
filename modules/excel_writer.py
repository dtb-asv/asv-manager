import openpyxl
import shutil
from datetime import datetime
from pathlib import Path
from openpyxl import load_workbook


class ExcelWriter:

    def __init__(self, sheet_name="ICS2"):
        self.sheet_name = sheet_name

    def _backup(self, excel_datei):
        backup = excel_datei.replace(
            ".xlsx",
            f"_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        shutil.copy2(excel_datei, backup)
        return backup

    def _headers(self, ws):
        headers = {}
        for col in range(1, ws.max_column + 1):
            headers[ws.cell(row=1, column=col).value] = col
        return headers

    def add_game(self, excel_datei, daten):
        backup = self._backup(excel_datei)

        wb = load_workbook(excel_datei)
        ws = wb[self.sheet_name]

        headers = self._headers(ws)
        neue_zeile = ws.max_row + 1

        for spalte, wert in daten.items():
            if spalte in headers:
                ws.cell(row=neue_zeile, column=headers[spalte]).value = wert

        wb.save(excel_datei)
        return backup

    def update_game(self, row_number, game_data):
        """
        Aktualisiert ein bestehendes Spiel in der Excel-Datei.
        row_number = echte Excel-Zeilennummer
        game_data = Dictionary mit den neuen Werten
        """

        wb = openpyxl.load_workbook(self.file_path)
        ws = wb["ICS2"]

        ws.cell(row=row_number, column=1).value = game_data.get("team", "")
        ws.cell(row=row_number, column=2).value = game_data.get("gegner", "")
        ws.cell(row=row_number, column=3).value = game_data.get("datum", "")
        ws.cell(row=row_number, column=4).value = game_data.get("uhrzeit", "")
        ws.cell(row=row_number, column=5).value = game_data.get("ort", "")
        ws.cell(row=row_number, column=6).value = game_data.get("bewerb", "")
        ws.cell(row=row_number, column=7).value = game_data.get("heim_auswaerts", "")

        wb.save(self.file_path)
        wb.close()

    def update_game(self, excel_datei, excel_zeile, daten):
        backup = self._backup(excel_datei)

        wb = load_workbook(excel_datei)
        ws = wb[self.sheet_name]

        headers = self._headers(ws)

        for spalte, wert in daten.items():
            if spalte in headers:
                ws.cell(row=excel_zeile, column=headers[spalte]).value = wert

        wb.save(excel_datei)
        return backup