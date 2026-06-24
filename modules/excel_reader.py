"""
=========================================================
ASV Manager
Excel Reader
=========================================================
"""

import pandas as pd


class ExcelReader:

    def __init__(self):
        self.df = None

    def load(self, datei, sheet="ICS2"):
        """Excel-Datei laden"""
        self.df = pd.read_excel(datei, sheet_name=sheet)

    def spiele(self):
        return len(self.df)

    def heimspiele(self):
        if "TYP" not in self.df.columns:
            return 0

        return len(
            self.df[
                self.df["TYP"].astype(str).str.lower() == "heim"
            ]
        )

    def auswaertsspiele(self):
        if "TYP" not in self.df.columns:
            return 0

        return len(
            self.df[
                self.df["TYP"].astype(str).str.lower() == "auswärts"
            ]
        )

    def mannschaften(self):
        if "LIGA" not in self.df.columns:
            return 0

        return self.df["LIGA"].nunique()

    def statistik(self):
        return {
            "Spiele": self.spiele(),
            "Heimspiele": self.heimspiele(),
            "Auswärtsspiele": self.auswaertsspiele(),
            "Mannschaften": self.mannschaften()
        }

    def naechstes_spiel(self):
        if self.df is None:
            return None

        if "DATUM" not in self.df.columns:
            return None

        df = self.df.copy()
        df["DATUM"] = pd.to_datetime(
            df["DATUM"],
            errors="coerce"
        )
        
        df = df.dropna(subset=["DATUM"])

        heute = pd.Timestamp.now().normalize()
        df = df[df["DATUM"] >= heute]

        if len(df) == 0:
            return None

        spiel = df.sort_values("DATUM").iloc[0]

        return {
            "liga": str(spiel.get("LIGA", "")),
            "datum": spiel["DATUM"].strftime("%d.%m.%Y"),
            "gegner": str(spiel.get("GEGNER", "")),
            "typ": str(spiel.get("TYP", "")),
            "ort": str(spiel.get("ORT", ""))
        }