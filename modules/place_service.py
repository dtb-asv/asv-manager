import pandas as pd

from modules.constants import (
    SHEET_PLACES,
    PREFIX_PLACE
)
from modules.facility_service import FacilityService
from modules.place_writer import PlaceWriter


class PlaceService:

    def __init__(self):

        self.writer = PlaceWriter()

    def load_places(self, excel_datei):

        df = pd.read_excel(
            excel_datei,
            sheet_name=SHEET_PLACES
        )

        if df.empty:
            return df

        if "AKTIV" in df.columns:
            df = df[df["AKTIV"] == "Ja"]

        return df.sort_values("NAME")

    def next_place_id(self, excel_datei):

        df = self.load_places(excel_datei)

        if df.empty:
            return f"{PREFIX_PLACE}000001"

        nummern = []

        for place_id in df["PLACE_ID"]:

            try:
                nummern.append(
                    int(
                        str(place_id).replace(
                            PREFIX_PLACE,
                            ""
                        )
                    )
                )
            except Exception:
                pass

        return f"{PREFIX_PLACE}{max(nummern)+1:06d}"

    def save_place(self, excel_datei, daten):

        if not daten.get("PLACE_ID"):

            daten["PLACE_ID"] = self.next_place_id(
                excel_datei
            )

            daten["AKTIV"] = "Ja"

            return self.writer.add_place(
                excel_datei,
                daten
            )

        self.writer.update_place(
            excel_datei,
            daten["PLACE_ID"],
            daten
        )

        return daten["PLACE_ID"]

    def archive_place(
        self,
        excel_datei,
        place_id
    ):

        self.writer.archive_place(
            excel_datei,
            place_id
        )

    def load_places_with_facility_name(self, excel_datei):

        places = self.load_places(excel_datei)
        facilities = FacilityService().load_facilities(excel_datei)

        if places.empty:
            return places

        return places.merge(
            facilities[["FACILITY_ID", "NAME"]],
            on="FACILITY_ID",
            how="left",
            suffixes=("", "_FACILITY")
        )    