import customtkinter as ctk
import pandas as pd

from modules.date_utils import parse_date, format_date, format_time


class GamesWindow(ctk.CTkToplevel):

    def __init__(self, parent, excel_datei):
        super().__init__(parent)

        self.excel_datei = excel_datei
        self.df_original = None

        self.title("Spiele Übersicht")
        self.geometry("1200x700")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="📅 Spiele Übersicht",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=15)

        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Suche nach Liga, Gegner, Ort..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        self.liga_filter = ctk.CTkOptionMenu(
            filter_frame,
            values=["Alle"],
            command=lambda _: self.apply_filter()
        )
        self.liga_filter.pack(side="left", padx=10)

        ctk.CTkButton(
            filter_frame,
            text="🔄 Aktualisieren",
            command=self.load_games
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            filter_frame,
            text="🔍 Suchen",
            command=self.apply_filter
        ).pack(side="left", padx=10)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_games()

    def load_games(self):
        df = pd.read_excel(self.excel_datei, sheet_name="ICS2")

        # komplett leere Zeilen entfernen
        df = df.dropna(how="all")

        # Zeilen ohne Liga und ohne Gegner ignorieren
        df = df[
            df["LIGA"].notna() |
            df["GEGNER"].notna()
        ]

        df["_DATUM_SORT"] = df["DATUM"].apply(parse_date)
        df = df.sort_values(by="_DATUM_SORT", na_position="last")

        self.df_original = df

        ligen = sorted(df["LIGA"].dropna().astype(str).unique().tolist())
        self.liga_filter.configure(values=["Alle"] + ligen)
        self.liga_filter.set("Alle")

        self.apply_filter()

    def apply_filter(self):
        df = self.df_original.copy()

        suche = self.search_entry.get().strip().lower()
        liga = self.liga_filter.get()

        if liga != "Alle":
            df = df[df["LIGA"].astype(str) == liga]

        if suche:
            df = df[
                df["LIGA"].astype(str).str.lower().str.contains(suche, na=False) |
                df["GEGNER"].astype(str).str.lower().str.contains(suche, na=False) |
                df["ORT"].astype(str).str.lower().str.contains(suche, na=False) |
                df["ART"].astype(str).str.lower().str.contains(suche, na=False) |
                df["STATUS"].astype(str).str.lower().str.contains(suche, na=False)
            ]

        self.show_table(df)

    def show_table(self, df):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        columns = ["LIGA", "DATUM", "STARTZEIT", "TYP", "ART", "GEGNER", "ORT", "STATUS"]

        for col_index, col in enumerate(columns):
            ctk.CTkLabel(
                self.scroll,
                text=col,
                font=("Segoe UI", 13, "bold")
            ).grid(row=0, column=col_index, padx=8, pady=6, sticky="w")

        for row_index, (_, row) in enumerate(df.iterrows(), start=1):
            values = [
                str(row.get("LIGA", "")),
                format_date(row.get("DATUM", "")),
                format_time(row.get("STARTZEIT", "")),
                str(row.get("TYP", "")),
                str(row.get("ART", "")),
                str(row.get("GEGNER", "")),
                str(row.get("ORT", "")),
                str(row.get("STATUS", "")),
            ]

            for col_index, value in enumerate(values):
                ctk.CTkLabel(
                    self.scroll,
                    text=value,
                    font=("Segoe UI", 12)
                ).grid(row=row_index, column=col_index, padx=8, pady=3, sticky="w")