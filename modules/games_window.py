import customtkinter as ctk
import pandas as pd

from modules.date_utils import parse_date, format_date, format_time


class GamesWindow(ctk.CTkToplevel):

    def __init__(self, parent, excel_datei):
        super().__init__(parent)

        self.excel_datei = excel_datei
        self.df_original = None
        self.selected_row = None
        self.selected_frame = None

        self.title("Spiele Übersicht")
        self.geometry("1200x720")
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
        self.search_entry.bind("<Return>",lambda event: self.apply_filter())

        self.liga_filter = ctk.CTkOptionMenu(
            filter_frame,
            values=["Alle"],
            command=lambda _: self.apply_filter()
        )
        self.liga_filter.pack(side="left", padx=10)

        ctk.CTkButton(
            filter_frame,
            text="🔍 Suchen",
            command=self.apply_filter
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            filter_frame,
            text="🔄 Aktualisieren",
            command=self.load_games
        ).pack(side="left", padx=10)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x", padx=20, pady=(0, 15))

        self.selection_label = ctk.CTkLabel(
            bottom,
            text="Kein Spiel ausgewählt",
            font=("Segoe UI", 14)
        )
        self.selection_label.pack(side="left", padx=10, pady=10)

        self.edit_button = ctk.CTkButton(
            bottom,
            text="✏️ Bearbeiten",
            command=self.bearbeiten_placeholder,
            state="disabled"
        )

        self.edit_button.pack(
            side="right",
            padx=10
        )

        self.load_games()

    def load_games(self):
        df = pd.read_excel(self.excel_datei, sheet_name="ICS2")

        df = df.dropna(how="all")

        df = df[
            df["LIGA"].notna() |
            df["GEGNER"].notna()
        ]

        df["_EXCEL_ROW"] = df.index + 2
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

        self.selected_row = None
        self.selected_frame = None
        self.selection_label.configure(text="Kein Spiel ausgewählt")
        self.edit_button.configure(state="disabled")

        columns = ["LIGA", "DATUM", "STARTZEIT", "TYP", "ART", "GEGNER", "ORT", "STATUS"]

        header = ctk.CTkFrame(self.scroll)
        header.pack(fill="x", pady=(0, 5))

        for col in columns:
            ctk.CTkLabel(
                header,
                text=col,
                width=120,
                font=("Segoe UI", 13, "bold")
            ).pack(side="left", padx=3)

        for _, row in df.iterrows():
            row_frame = ctk.CTkFrame(self.scroll)
            row_frame.pack(fill="x", pady=2)

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

            for value in values:
                label = ctk.CTkLabel(
                    row_frame,
                    text=value,
                    width=120,
                    font=("Segoe UI", 12)
                )
                label.pack(side="left", padx=3)

                label.bind(
                    "<Button-1>",
                    lambda event, r=row, f=row_frame: self.select_row(r, f)
                )

                label.bind(
                    "<Double-Button-1>",
                    lambda event: self.bearbeiten_placeholder()
                )

            row_frame.bind(
                "<Button-1>",
                lambda event, r=row, f=row_frame: self.select_row(r, f)
            )

            row_frame.bind(
                "<Double-Button-1>",
                lambda event: self.bearbeiten_placeholder()
            )

    def select_row(self, row, frame):
        if self.selected_frame:
            self.selected_frame.configure(fg_color="transparent")

        self.selected_frame = frame
        self.selected_row = row

        frame.configure(fg_color="#3A3A3A")

        text = (
            f"Ausgewählt: {row.get('LIGA', '')} | "
            f"{format_date(row.get('DATUM', ''))} | "
            f"{row.get('GEGNER', '')}"
        )
        self.edit_button.configure(state="normal")
        self.selection_label.configure(text=text)

    def bearbeiten_placeholder(self):
        if self.selected_row is None:
            self.selection_label.configure(
                text="Bitte zuerst ein Spiel auswählen."
            )
            return

        from modules.add_game_window import AddGameWindow

        AddGameWindow(
            self,
            self.excel_datei,
            on_saved=self.load_games,
            edit_data=self.selected_row
        )