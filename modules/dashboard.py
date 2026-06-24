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
            font=("Segoe UI", 22, "bold")
        )
        self.title.pack(pady=(10, 15))

        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(fill="x", padx=10, pady=5)

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
            row.pack(fill="x", pady=2)

            label_name = ctk.CTkLabel(
                row,
                text=feld,
                font=("Segoe UI", 14)
            )
            label_name.pack(side="left", padx=10)

            label_value = ctk.CTkLabel(
                row,
                text="-",
                font=("Segoe UI", 14, "bold")
            )
            label_value.pack(side="right", padx=10)

            self.labels[feld] = label_value

        self.next_game_frame = ctk.CTkFrame(self)
        self.next_game_frame.pack(fill="x", padx=10, pady=(10, 10))

        self.next_game_title = ctk.CTkLabel(
            self.next_game_frame,
            text="📅 Nächstes Spiel",
            font=("Segoe UI", 16, "bold")
        )
        self.next_game_title.pack(pady=(8, 4))

        self.next_game_label = ctk.CTkLabel(
            self.next_game_frame,
            text="Noch keine Daten geladen",
            justify="left",
            font=("Segoe UI", 13),
            wraplength=520
        )
        self.next_game_label.pack(padx=10, pady=(0, 10))

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

        typ = str(spiel.get("typ", "")).strip().lower()

        if typ == "heim":
            begegnung = f"ASV Neufeld vs {spiel['gegner']}"
        else:
            begegnung = f"{spiel['gegner']} vs ASV Neufeld"

        text = (
            f"{spiel['liga']} | {spiel['datum']}\n"
            f"{begegnung}\n"
            f"📍 {spiel['ort']}"
        )

        self.next_game_label.configure(text=text)