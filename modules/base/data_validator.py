import pandas as pd


class DataValidator:

    def check_duplicate_ids(
        self,
        excel_datei,
        sheet_name,
        id_column
    ):

        df = pd.read_excel(
            excel_datei,
            sheet_name=sheet_name
        )

        if df.empty:
            return []

        if id_column not in df.columns:
            return []

        duplicates = df[
            df[id_column].duplicated(keep=False)
        ]

        if duplicates.empty:
            return []

        return duplicates[id_column].dropna().unique().tolist()

    def print_duplicate_report(
        self,
        excel_datei,
        sheet_name,
        id_column
    ):

        duplicates = self.check_duplicate_ids(
            excel_datei,
            sheet_name,
            id_column
        )

        if duplicates:

            print(f"\n⚠️ Doppelte IDs in {sheet_name}")

            for duplicate in duplicates:
                print(f"   - {duplicate}")

        else:

            print(f"✅ {sheet_name}: keine doppelten IDs")    