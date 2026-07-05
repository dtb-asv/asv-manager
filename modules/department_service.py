import pandas as pd

from modules.constants import (
    SHEET_DEPARTMENTS,
    PREFIX_DEPARTMENT
)

from modules.department_writer import DepartmentWriter


class DepartmentService:

    def __init__(self):

        self.writer = DepartmentWriter()

    def load_departments(self, excel_datei):

        df = pd.read_excel(
            excel_datei,
            sheet_name=SHEET_DEPARTMENTS
        )

        if df.empty:
            return df

        if "AKTIV" in df.columns:
            df = df[df["AKTIV"] == "Ja"]

        return df.sort_values("NAME")

    def next_department_id(self, excel_datei):

        df = self.load_departments(excel_datei)

        if df.empty:
            return f"{PREFIX_DEPARTMENT}000001"

        nummern = []

        for department_id in df["DEPARTMENT_ID"]:

            try:
                nummern.append(
                    int(
                        str(department_id).replace(
                            PREFIX_DEPARTMENT,
                            ""
                        )
                    )
                )
            except Exception:
                pass

        return f"{PREFIX_DEPARTMENT}{max(nummern)+1:06d}"

    def save_department(self, excel_datei, daten):

        if not daten.get("DEPARTMENT_ID"):

            daten["DEPARTMENT_ID"] = self.next_department_id(
                excel_datei
            )

            daten["AKTIV"] = "Ja"

            return self.writer.add_department(
                excel_datei,
                daten
            )

        self.writer.update_department(
            excel_datei,
            daten["DEPARTMENT_ID"],
            daten
        )

        return daten["DEPARTMENT_ID"]

    def archive_department(
        self,
        excel_datei,
        department_id
    ):

        self.writer.archive_department(
            excel_datei,
            department_id
        )