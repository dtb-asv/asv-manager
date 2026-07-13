import pandas as pd


class ServiceBase:

    def load_sheet(self, excel_datei, sheet_name):

        return pd.read_excel(
            excel_datei,
            sheet_name=sheet_name
        )

    def active_only(self, df, status_column="AKTIV"):

        if df.empty:
            return df

        if status_column not in df.columns:
            return df

        return df[
            df[status_column]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["ja", "true", "1", "aktiv"])
        ]