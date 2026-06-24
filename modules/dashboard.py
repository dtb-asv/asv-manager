"""
Dashboard Widget
"""

import customtkinter as ctk


class Dashboard(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.pack(fill="x", padx=20, pady=10)

        self.title = ctk.CTkLabel(
            self,
            text="Saisonübersicht",
            font=("Segoe UI", 24, "bold")
        )
        self.title.pack(pady=(10, 20))

        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(fill="x", padx=10, pady=10)

        self.labels = {}

        felder = [
            "Spiele",
            "Heimspiele",
            "Auswärtsspiele",
            "Mannschaften",
            "Diese Woche",
            "Freundschaftsspiele",
            "Abgesagt"
        ]

        for feld in felder:
            row = ctk.CTkFrame(self.stats_frame)
            row.pack(fill="x", pady=5)

            label_name = ctk.CTkLabel(
                row,
                text=feld,
                font=("Segoe UI", 16)
            )
            label_name.pack(side="left", padx=10)

            label_value = ctk.CTkLabel(
                row,
                text="-",
                font=("Segoe UI", 16, "bold")
            )
            label_value.pack(side="right", padx=10)

            self.labels[feld] = label_value

        self.next_game_frame = ctk.CTkFrame(self)
        self.next_game_frame.pack(fill="x", padx=10, pady=20)

        self.next_game_title = ctk.CTkLabel(
            self.next_game_frame,
            text="📅 Nächstes Spiel",
            font=("Segoe UI", 18, "bold")
        )
        self.next_game_title.pack(pady=(10, 5))

        self.next_game_label = ctk.CTkLabel(
            self.next_game_frame,
            text="Noch keine Daten geladen",
            justify="left",
            font=("Segoe UI", 15)
        )
        self.next_game_label.pack(pady=(0, 10))

    def update_stats(self, stats):
        for key, value in stats.items():
            if key in self.labels:
                self.labels[key].configure(text=str(value))

    def update_next_game(self, spiel):
        if spiel is None:
            self.next_game_label.configure(
                text="Kein zukünftiges Spiel gefunden"
            )
            return

        text = (
            f"{spiel['liga']}\n\n"
            f"{spiel['datum']}\n\n"
            f"ASV Neufeld vs {spiel['gegner']}\n\n"
            f"📍 {spiel['ort']}"
        )

        self.next_game_label.configure(text=text)