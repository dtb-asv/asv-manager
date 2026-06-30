import pandas as pd

from modules.configuration_service import ConfigurationService
from modules.constants import SHEET_CFG_LOOKUPS
from modules.lookup_writer import LookupWriter


class LookupService:

    def __init__(self):
        self.configuration_service = ConfigurationService()
        self.writer = LookupWriter()

    def load_all(self, excel_datei):
        self.configuration_service.ensure_configuration_sheets(excel_datei)

        return pd.read_excel(
            excel_datei,
            sheet_name=SHEET_CFG_LOOKUPS
        )

    def load_by_type(self, excel_datei, lookup_type):
        df = self.load_all(excel_datei)

        df = df.dropna(how="all")

        return df[
            df["LOOKUP_TYPE"].astype(str).str.upper() == lookup_type.upper()
        ]

    def get_lookup_list(self, excel_datei, lookup_type):

        df = self.load_by_type(
            excel_datei,
            lookup_type
        )

        if len(df) == 0:
            return []

        df = df.sort_values("SORTIERUNG")

        return df["NAME"].tolist()   

    def add_lookup(self, excel_datei, daten):

        daten["LOOKUP_ID"] = self.next_lookup_id(excel_datei)

        self.writer.add_lookup(
            excel_datei,
            daten
        )


    def update_lookup(
        self,
        excel_datei,
        lookup_id,
        daten
    ):

        self.writer.update_lookup(
            excel_datei,
            lookup_id,
            daten
        )


    def archive_lookup(
        self,
        excel_datei,
        lookup_id
    ):

        self.writer.archive_lookup(
            excel_datei,
            lookup_id
        )    

    def next_lookup_id(self, excel_datei):

        df = self.load_all(excel_datei)

        if df.empty or "LOOKUP_ID" not in df.columns:
            return "LOOKUP000001"

        nummern = []

        for value in df["LOOKUP_ID"].dropna():

            text = str(value)

            if text.startswith("LOOKUP"):

                try:
                    nummern.append(
                        int(text.replace("LOOKUP", ""))
                    )
                except ValueError:
                    pass

        next_number = max(nummern, default=0) + 1

        return f"LOOKUP{next_number:06d}"     