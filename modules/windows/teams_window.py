import customtkinter as ctk

from modules.services.team_service import TeamService


class TeamsWindow(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.service = TeamService()

        self.title("Mannschaften")
        self.geometry("900x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Überschrift
        title = ctk.CTkLabel(
            self,
            text="Mannschaften",
            font=("Segoe UI", 22, "bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Tabellenbereich (vorerst Platzhalter)
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="nsew"
        )

        # Footer
        footer = ctk.CTkFrame(self)
        footer.grid(
            row=2,
            column=0,
            padx=20,
            pady=20,
            sticky="ew"
        )

        close_btn = ctk.CTkButton(
            footer,
            text="Schließen",
            command=self.destroy
        )

        close_btn.pack(side="right")

        self.refresh()

    def refresh(self):

        # Alte Einträge entfernen
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        teams = self.service.get_all()

        # Tabellenkopf
        header = ctk.CTkFrame(self.table_frame)
        header.pack(fill="x", padx=5, pady=(5, 2))

        headers = [
            ("Mannschaft", 250),
            ("Saison", 120),
            ("Aktiv", 80),
        ]

        for text, width in headers:
            lbl = ctk.CTkLabel(
                header,
                text=text,
                width=width,
                anchor="w",
                font=("Segoe UI", 13, "bold")
            )
            lbl.pack(side="left", padx=5)

        # Daten
        for team in teams:

            row = ctk.CTkFrame(self.table_frame)
            row.pack(fill="x", padx=5, pady=1)

            ctk.CTkLabel(
                row,
                text=team["name"],
                width=250,
                anchor="w"
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                row,
                text=str(team["season_id"]),
                width=120,
                anchor="w"
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                row,
                text="Ja" if team["active"] else "Nein",
                width=80,
                anchor="w"
            ).pack(side="left", padx=5)