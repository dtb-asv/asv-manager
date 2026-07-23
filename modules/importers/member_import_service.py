import pandas as pd


class MemberImportService:
    """
    Liest die Mitglieder-Excel und erstellt
    eine bereinigte Importvorschau.
    """

    SHEET_NAME = "MB 2026_27"

    REQUIRED_COLUMNS = [
        "ID",
        "Vorname",
        "Nachname",
        "Geburtstag",
    ]

    def load_preview(self, filename):
        df = pd.read_excel(
            filename,
            sheet_name=self.SHEET_NAME,
            header=1
        )

        df = df.dropna(how="all")

        missing_columns = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                "Folgende Pflichtspalten fehlen: "
                + ", ".join(missing_columns)
            )

        df = df[self.REQUIRED_COLUMNS].copy()
        df["ID"] = (
            pd.to_numeric(df["ID"], errors="coerce")
            .astype("Int64")
        )

        df["Vorname"] = (
            df["Vorname"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df["Nachname"] = (
            df["Nachname"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df["Geburtstag"] = pd.to_datetime(
            df["Geburtstag"],
            dayfirst=True,
            errors="coerce"
        ).dt.date

        df = df[
            (df["Vorname"] != "")
            & (df["Nachname"] != "")
        ].copy()

        return df.reset_index(drop=True)

    def statistics(self, df):
        duplicate_mask = df.duplicated(
            subset=["Vorname", "Nachname", "Geburtstag"],
            keep=False
        )

        return {
            "rows": len(df),
            "valid_birth_dates": int(
                df["Geburtstag"].notna().sum()
            ),
            "missing_birth_dates": int(
                df["Geburtstag"].isna().sum()
            ),
            "duplicates": int(
                duplicate_mask.sum()
            ),
            "columns": list(df.columns),
        }