import customtkinter as ctk
from modules.team_service import TeamService
from tkinter import messagebox
from modules.widgets.change_reason_dialog import ChangeReasonDialog


class TeamWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        excel_datei,
        on_saved=None,
        team_data=None
    ):

        super().__init__(parent)

        self.excel_datei = excel_datei
        self.on_saved = on_saved
        self.service = TeamService()
        self.team_data = team_data

        if team_data:
            self.title("Mannschaft bearbeiten")
        else:
            self.title("Neue Mannschaft")
        self.geometry("500x450")

        self.grab_set()

        titel = "⚽ Neue Mannschaft"

        if team_data:
            titel = "✏ Mannschaft bearbeiten"

        ctk.CTkLabel(
            self,
            text=titel,
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Mannschaft"
        ).pack(anchor="w", padx=20)

        self.name = ctk.CTkEntry(
            self,
            width=300
        )

        self.name.pack(
            padx=20,
            pady=(0, 10)
        )

        ctk.CTkLabel(
            self,
            text="Saison"
        ).pack(anchor="w", padx=20)

        self.saison = ctk.CTkComboBox(
            self,
            width=300,
            values=[
                "2025/2026",
                "2026/2027",
                "2027/2028"
            ]
        )
        self.saison.pack(
            padx=20,
            pady=(0, 10)
        )

        self.saison.set("2026/2027")

        ctk.CTkLabel(
            self,
            text="Typ"
        ).pack(anchor="w", padx=20)

        self.typ = ctk.CTkComboBox(
            self,
            width=300,
            values=[
                "Normal",
                "Spielgemeinschaft",
                "Mädchen",
                "Fußballkindergarten"
            ]
        )

        self.typ.pack(
            padx=20,
            pady=(0, 20)
        )

        self.typ.set("Normal")

        if self.team_data:

            self.name.insert(
                0,
                self.team_data.get("MANNSCHAFT", "")
            )

            self.saison.set(
                self.team_data.get("SAISON", "2026/2027")
            )

            self.typ.set(
                self.team_data.get("TYP", "Normal")
            )
        

        ctk.CTkButton(
            self,
            text="Speichern",
            command=self.speichern
        ).pack(pady=20)

    def speichern(self):

        name = self.name.get().strip()

        if not name:
            messagebox.showwarning(
                "Fehlende Eingabe",
                "Bitte einen Mannschaftsnamen eingeben.",
                parent=self
            )
            return

        daten = {
            "MANNSCHAFT": name,
            "SAISON": self.saison.get(),
            "TYP": self.typ.get()
        }

        if self.team_data:

            dialog = ChangeReasonDialog(
                self,
                title="Mannschaft ändern"
            )

            self.wait_window(dialog)

            if dialog.result is None:
                return

            daten["_GRUND"] = dialog.result["grund"]
            daten["_BEMERKUNG"] = dialog.result["bemerkung"]

            self.service.update_team(
                self.excel_datei,
                self.team_data["TEAM_ID"],
                daten
            )

        else:

            self.service.add_team(
                self.excel_datei,
                daten
            )

        if self.on_saved:
            self.on_saved()

        self.destroy()  