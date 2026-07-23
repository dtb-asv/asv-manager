"""
Dashboard Widget
"""

import customtkinter as ctk


class Dashboard(ctk.CTkFrame):

    def __init__(
        self,
        master,
        on_open_training_schedules=None,
        on_sync_trainings=None
    ):
        super().__init__(master)

        self.on_open_training_schedules = on_open_training_schedules
        self.on_sync_trainings = on_sync_trainings

        self.pack(fill="both", expand=True, padx=20, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(10, 15)
        )

        ctk.CTkLabel(
            header,
            text="⚽ ASV Manager",
            font=("Segoe UI", 26, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Vereinsübersicht und aktuelle Aufgaben",
            font=("Segoe UI", 13),
            text_color=("gray40", "gray70")
        ).pack(anchor="w", pady=(3, 0))

        self.stats_card = ctk.CTkFrame(self)
        self.stats_card.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(10, 5),
            pady=5
        )

        ctk.CTkLabel(
            self.stats_card,
            text="📅 Heute & Diese Woche",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=18, pady=(15, 10))

        self.labels = {}

        felder = [
            "Spiele diese Woche",
            "Trainings diese Woche",
            "Trainings heute",
            "Nächstes Spiel",
            "Nächstes Training",
            "Offene Aufgaben",
            "Konflikte"
        ]

        for feld in felder:
            row = ctk.CTkFrame(
                self.stats_card,
                fg_color="transparent"
            )
            row.pack(fill="x", padx=12, pady=2)

            ctk.CTkLabel(
                row,
                text=feld,
                font=("Segoe UI", 13)
            ).pack(side="left", padx=6)

            label_value = ctk.CTkLabel(
                row,
                text="-",
                font=("Segoe UI", 13, "bold")
            )
            label_value.pack(side="right", padx=6)

            self.labels[feld] = label_value

        self.next_game_card = ctk.CTkFrame(self)
        self.next_game_card.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=5
        )

        ctk.CTkLabel(
            self.next_game_card,
            text="📅 Nächstes Spiel",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=18, pady=(15, 10))

        self.next_game_label = ctk.CTkLabel(
            self.next_game_card,
            text="Noch keine Daten geladen",
            justify="left",
            anchor="w",
            font=("Segoe UI", 14),
            wraplength=420
        )
        self.next_game_label.pack(
            fill="x",
            padx=18,
            pady=(5, 15)
        )

        self.training_card = ctk.CTkFrame(self)
        self.training_card.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(10, 5)
        )

        training_header = ctk.CTkFrame(
            self.training_card,
            fg_color="transparent"
        )
        training_header.pack(
            fill="x",
            padx=18,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            training_header,
            text="⚽ Trainingsplanung",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left")

        self.training_status_label = ctk.CTkLabel(
            training_header,
            text="Bereit",
            font=("Segoe UI", 12),
            text_color=("gray40", "gray70")
        )
        self.training_status_label.pack(side="right")

        training_info = ctk.CTkFrame(
            self.training_card,
            fg_color="transparent"
        )
        training_info.pack(
            fill="x",
            padx=18,
            pady=(5, 10)
        )

        self.active_schedules_label = self._create_info_block(
            training_info,
            "Aktive Trainingspläne",
            "-"
        )

        self.pending_trainings_label = self._create_info_block(
            training_info,
            "Noch zu erzeugen",
            "-"
        )

        self.last_sync_label = self._create_info_block(
            training_info,
            "Letzte Synchronisierung",
            "-"
        )

        training_buttons = ctk.CTkFrame(
            self.training_card,
            fg_color="transparent"
        )
        training_buttons.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        self.open_schedules_button = ctk.CTkButton(
            training_buttons,
            text="Trainingspläne öffnen",
            width=180,
            command=self._open_training_schedules
        )
        self.open_schedules_button.pack(
            side="left",
            padx=(0, 10)
        )

        self.sync_trainings_button = ctk.CTkButton(
            training_buttons,
            text="Trainings synchronisieren",
            width=190,
            command=self._sync_trainings
        )
        self.sync_trainings_button.pack(side="left")

    def _create_info_block(
        self,
        parent,
        title,
        value
    ):

        block = ctk.CTkFrame(parent)
        block.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        ctk.CTkLabel(
            block,
            text=title,
            font=("Segoe UI", 12),
            text_color=("gray40", "gray70")
        ).pack(anchor="w", padx=12, pady=(10, 2))

        value_label = ctk.CTkLabel(
            block,
            text=value,
            font=("Segoe UI", 18, "bold")
        )
        value_label.pack(anchor="w", padx=12, pady=(0, 10))

        return value_label

    def _open_training_schedules(self):

        if callable(self.on_open_training_schedules):
            self.on_open_training_schedules()
            return

        self.training_status_label.configure(
            text="Trainingsplan-Fenster noch nicht verbunden"
        )

    def _sync_trainings(self):

        if callable(self.on_sync_trainings):
            self.on_sync_trainings()
            return

        self.training_status_label.configure(
            text="Synchronisierung noch nicht verbunden"
        )

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
        gegner = str(spiel.get("gegner", "")).strip()

        if typ == "heim":
            begegnung = f"ASV Neufeld vs {gegner}"
        else:
            begegnung = f"{gegner} vs ASV Neufeld"

        text = (
            f"{spiel.get('liga', '')} | "
            f"{spiel.get('datum', '')}\n"
            f"{begegnung}\n"
            f"📍 {spiel.get('ort', '')}"
        )

        self.next_game_label.configure(text=text)

    def update_training_overview(
        self,
        active_schedules=None,
        pending_trainings=None,
        last_sync=None,
        status=None
    ):

        if active_schedules is not None:
            self.active_schedules_label.configure(
                text=str(active_schedules)
            )

        if pending_trainings is not None:
            self.pending_trainings_label.configure(
                text=str(pending_trainings)
            )

        if last_sync is not None:
            self.last_sync_label.configure(
                text=str(last_sync)
            )

        if status is not None:
            self.training_status_label.configure(
                text=str(status)
            )
