import pandas as pd

from modules.constants import (
    SHEET_FACILITIES,
    PREFIX_FACILITY
)
from modules.facility_writer import FacilityWriter


class FacilityService:

    def __init__(self):

        self.writer = FacilityWriter()

    def load_facilities(self, excel_datei):

        df = pd.read_excel(
            excel_datei,
            sheet_name=SHEET_FACILITIES
        )

        if df.empty:
            return df

        if "AKTIV" in df.columns:
            df = df[df["AKTIV"] == "Ja"]

        return df.sort_values("NAME")

    def next_facility_id(self, excel_datei):

        df = self.load_facilities(excel_datei)

        if df.empty:
            return f"{PREFIX_FACILITY}000001"

        nummern = []

        for facility_id in df["FACILITY_ID"]:

            try:
                nummern.append(
                    int(
                        str(facility_id).replace(
                            PREFIX_FACILITY,
                            ""
                        )
                    )
                )
            except Exception:
                pass

        return f"{PREFIX_FACILITY}{max(nummern)+1:06d}"

    def save_facility(self, excel_datei, daten):

        if not daten.get("FACILITY_ID"):

            daten["FACILITY_ID"] = self.next_facility_id(
                excel_datei
            )

            daten["AKTIV"] = "Ja"

            return self.writer.add_facility(
                excel_datei,
                daten
            )

        self.writer.update_facility(
            excel_datei,
            daten["FACILITY_ID"],
            daten
        )

        return daten["FACILITY_ID"]

    def archive_facility(
        self,
        excel_datei,
        facility_id
    ):

        self.writer.archive_facility(
            excel_datei,
            facility_id
        )