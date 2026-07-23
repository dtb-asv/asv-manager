import customtkinter as ctk

from modules.team_service import TeamService
from modules.team_window import TeamWindow
from tkinter import messagebox
from modules.widgets.search_bar import SearchBar



class TeamsWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.service = TeamService()
        self.selected_team = None
        self.selected_frame = None
       
        self.title("Mannschaften")
        self.geometry("1000x650")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="⚽ Mannschaften",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=20)

        toolbar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        toolbar.pack(pady=5)

        self.search = SearchBar(
            self,
            callback=self.filter_teams,
            placeholder="Mannschaften suchen..."
        )

        self.search.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        ctk.CTkButton(
            toolbar,
            text="➕ Neu",
            command=self.neue_mannschaft,
            width=140
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="✏ Bearbeiten",
            command=self.bearbeiten_team,
            width=140
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="📦 Archivieren",
            command=self.archivieren_team,
            width=140
        ).pack(side="left", padx=5)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            self,
            text="❌ Schließen",
            command=self.destroy
        ).pack(pady=15)

        self.load_teams()

    def load_teams(self):

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.selected_team = None
        self.selected_frame = None

        teams = self.service.get_active()

        import pandas as pd

        rows = []

        for team in teams:
            rows.append({
                "TEAM_ID": team["team_id"],
                "NAME": team["name"],
                "ALTERSKLASSE": "",
                "NAME_DEPARTMENT": "",
                "SEASON_ID": team["season_id"],
                "ACTIVE": team["active"],
            })

        self.df = pd.DataFrame(rows)

        if self.df.empty:

            ctk.CTkLabel(
                self.scroll,
                text="Noch keine Mannschaften vorhanden.",
                font=("Segoe UI", 15)
            ).pack(pady=20)

            return

        self.draw_teams(self.df)
                        
    def draw_teams(self, df):  

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.selected_team = None
        self.selected_frame = None

        columns = [
            "TEAM_ID",
            "NAME",
            "ALTERSKLASSE",
            "NAME_DEPARTMENT"
        ]

        header = ctk.CTkFrame(self.scroll)
        header.pack(fill="x")

        for col in columns:
            ctk.CTkLabel(
                header,
                text=col,
                width=180,
                font=("Segoe UI", 13, "bold")
            ).pack(side="left", padx=3)

        for _, row in df.iterrows():

            row_data = row.to_dict()

            frame = ctk.CTkFrame(
                self.scroll,
                fg_color="transparent"
            )
            frame.pack(fill="x", pady=2)

            frame.bind(
                "<Button-1>",
                lambda event, r=row_data, f=frame: self.select_team(r, f)
            )

            frame.bind(
                "<Double-Button-1>",
                lambda event: self.bearbeiten_team()
            )

            for col in columns:

                label = ctk.CTkLabel(
                    frame,
                    text=str(row.get(col, "")),
                    width=180
                )
                label.pack(side="left", padx=3)

                label.bind(
                    "<Button-1>",
                    lambda event, r=row_data, f=frame: self.select_team(r, f)
                )     

                label.bind(
                    "<Double-Button-1>",
                    lambda event: self.bearbeiten_team()
                )     

    def neue_mannschaft(self):

       TeamWindow(
            self,
            on_saved=self.load_teams
        )

    def bearbeiten_team(self):

        if self.selected_team is None:
            messagebox.showwarning(
                "Keine Mannschaft",
                "Bitte zuerst eine Mannschaft auswählen.",
                parent=self
            )
            return

        TeamWindow(
            self,
            on_saved=self.load_teams,
            team_data=self.selected_team
        )

    def archivieren_team(self):

        if self.selected_team is None:
            messagebox.showwarning(
                "Keine Mannschaft",
                "Bitte zuerst eine Mannschaft auswählen.",
                parent=self
            )
            return

        antwort = messagebox.askyesno(
            "Mannschaft archivieren",
            f"Soll {self.selected_team['NAME']} archiviert werden?",
            parent=self
        )

        if not antwort:
            return

        self.service.archive_team(
            self.excel_datei,
            self.selected_team["TEAM_ID"]
        )

        self.load_teams()

    def select_team(self, row, frame):

        if self.selected_frame:
            self.selected_frame.configure(
                fg_color="transparent"
            )

        frame.configure(
            fg_color=("lightblue", "#1F538D")
        )

        self.selected_frame = frame
        self.selected_team = row

        print(self.selected_team)    

    def filter_teams(self, text):

        text = text.strip().lower()

        if text == "":
            self.load_teams()
            return

        df = self.df.copy()

        mask = (
            df["NAME"].astype(str).str.lower().str.contains(text)
            |
            df["TEAM_ID"].astype(str).str.lower().str.contains(text)
            |
            df["ALTERSKLASSE"].astype(str).str.lower().str.contains(text)
            |
            df["NAME_DEPARTMENT"].astype(str).str.lower().str.contains(text)
        )

        self.draw_teams(df[mask])       
