"""
=========================================================
ASV Manager
Excel Reader
=========================================================
Liest Excel-Daten und liefert Statistiken.
"""

import pandas as pd

from modules.date_utils import parse_date


class ExcelReader:

    def __init__(self):
        # Spiele (Kompatibilität)
        self.df = None
        self.games = None

        # Trainings
        self.trainings = None
        self.training_schedules = None

        # Stammdaten
        self.teams = None
        self.places = None
        self.trainers = None
        self.members = None

    def load(self, datei, sheet="ICS2"):
        """
        Lädt alle verfügbaren Tabellen der Vereinsdatei.
        Fehlende Tabellen sind erlaubt.
        """

        def load_sheet(name):
            try:
                return pd.read_excel(datei, sheet_name=name)
            except Exception:
                return pd.DataFrame()

        # Spiele
        self.games = load_sheet(sheet)
        self.df = self.games        # Kompatibilität

        # Training
        self.trainings = load_sheet("TRAININGS")
        self.training_schedules = load_sheet("TRAINING_SCHEDULES")

        # Stammdaten
        self.teams = load_sheet("TEAMS")
        self.places = load_sheet("PLACES")
        self.trainers = load_sheet("TRAINERS")
        self.members = load_sheet("MEMBERS")

    def spiele(self):
        return len(self.df)

    def heimspiele(self):
        if "TYP" not in self.df.columns:
            return 0

        return len(
            self.df[self.df["TYP"].astype(str).str.lower() == "heim"]
        )

    def auswaertsspiele(self):
        if "TYP" not in self.df.columns:
            return 0

        return len(
            self.df[self.df["TYP"].astype(str).str.lower() == "auswärts"]
        )

    def mannschaften(self):
        if "LIGA" not in self.df.columns:
            return 0

        return self.df["LIGA"].nunique()

    def abgesagt(self):
        if "STATUS" not in self.df.columns:
            return 0

        return len(
            self.df[self.df["STATUS"].astype(str).str.lower() == "abgesagt"]
        )

    def freundschaftsspiele(self):
        if "STATUS" not in self.df.columns:
            return 0

        status = self.df["STATUS"].astype(str).str.lower()

        return len(
            self.df[
                status.isin(["fs", "freundschaft", "freundschaftsspiel"])
            ]
        )

    def spiele_diese_woche(self):
        if "DATUM" not in self.df.columns:
            return 0

        df = self.df.copy()
        df["DATUM_SORT"] = df["DATUM"].apply(parse_date)
        df = df.dropna(subset=["DATUM_SORT"])

        heute = pd.Timestamp.now().normalize()
        montag = heute - pd.Timedelta(days=heute.weekday())
        sonntag = montag + pd.Timedelta(days=6)

        df = df[
            (df["DATUM_SORT"] >= montag) &
            (df["DATUM_SORT"] <= sonntag)
        ]

        return len(df)

    def statistik(self):
        return {
            "Spiele": self.spiele(),
            "Heimspiele": self.heimspiele(),
            "Auswärtsspiele": self.auswaertsspiele(),
            "Mannschaften": self.mannschaften(),
            "Diese Woche": self.spiele_diese_woche(),
            "Freundschaftsspiele": self.freundschaftsspiele(),
            "Abgesagt": self.abgesagt()
        }

    def naechstes_spiel(self):
        if self.df is None:
            return None

        if "DATUM" not in self.df.columns:
            return None

        df = self.df.copy()
        df["DATUM_SORT"] = df["DATUM"].apply(parse_date)
        df = df.dropna(subset=["DATUM_SORT"])

        heute = pd.Timestamp.now().normalize()
        df = df[df["DATUM_SORT"] >= heute]

        if len(df) == 0:
            return None

        spiel = df.sort_values("DATUM_SORT").iloc[0]

        return {
            "liga": str(spiel.get("LIGA", "")),
            "datum": spiel["DATUM_SORT"].strftime("%d.%m.%Y"),
            "gegner": str(spiel.get("GEGNER", "")),
            "typ": str(spiel.get("TYP", "")),
            "ort": str(spiel.get("ORT", ""))
        }

    def trainings_statistik(self):
        """
        Liefert Trainingsinformationen für das Dashboard.
        """

        from datetime import date, timedelta
        import pandas as pd

        heute = date.today()
        montag = heute - timedelta(days=heute.weekday())
        sonntag = montag + timedelta(days=6)

        result = {
            "heute": 0,
            "woche": 0,
            "aktive_plaene": 0
        }

        # ---------------------------------
        # konkrete Trainings
        # ---------------------------------

        if hasattr(self, "trainings") and self.trainings is not None:

            if not self.trainings.empty:

                df = self.trainings.copy()

                if "DATUM" in df.columns:

                    df["DATUM"] = pd.to_datetime(
                        df["DATUM"],
                        dayfirst=True,
                        errors="coerce"
                    ).dt.date

                    result["heute"] = len(
                        df[df["DATUM"] == heute]
                    )

                    result["woche"] = len(
                        df[
                            (df["DATUM"] >= montag)
                            &
                            (df["DATUM"] <= sonntag)
                        ]
                    )

        # ---------------------------------
        # Trainingspläne
        # ---------------------------------

        if hasattr(self, "training_schedules"):

            if self.training_schedules is not None:

                if not self.training_schedules.empty:

                    df = self.training_schedules

                    if "AKTIV" in df.columns:

                        result["aktive_plaene"] = len(
                            df[
                                df["AKTIV"]
                                .astype(str)
                                .str.upper()
                                .isin(["JA", "TRUE", "1", "AKTIV"])
                            ]
                        )
                    else:
                        result["aktive_plaene"] = len(df)

        return result    

    def naechstes_training(self):
        """
        Liefert das nächste geplante Training.
        """

        from datetime import datetime
        import pandas as pd

        if not hasattr(self, "trainings"):
            return None

        if self.trainings is None or self.trainings.empty:
            return None

        df = self.trainings.copy()

        if "DATUM" not in df.columns:
            return None

        df["DATUM"] = pd.to_datetime(
            df["DATUM"],
            dayfirst=True,
            errors="coerce"
        )

        jetzt = datetime.now()

        df = df[df["DATUM"] >= jetzt]

        if df.empty:
            return None

        df = df.sort_values("DATUM")

        return df.iloc[0].to_dict()    