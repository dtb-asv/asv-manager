import customtkinter as ctk
import pandas as pd

from modules.widgets.list_window_base import ListWindowBase
from modules.place_service import PlaceService
from modules.place_dialog import PlaceDialog
from tkinter import messagebox



class PlaceWindow(ListWindowBase):

    def __init__(self, parent):

        self.service = PlaceService()

        super().__init__(
            parent,
            title="Plätze",
            icon="⚽",
            search_placeholder="Platz suchen...",
            search_callback=self.load_data
        )

        self.add_toolbar_button(
            "➕ Neu",
            self.neuer_platz
        )

        self.add_toolbar_button(
            "✏ Bearbeiten",
            self.bearbeiten_platz
        )

        self.add_toolbar_button(
            "📦 Archivieren",
            self.archivieren_platz
        )

        self.add_toolbar_button(
            "🔄 Aktualisieren",
            self.refresh
        )

        self.load_data()

        
    def load_data(self, suchtext=""):

        df = pd.DataFrame(
            self.service.get_active()
        )

        if suchtext and not df.empty:
            df = df[
                df["name"].str.contains(
                    suchtext,
                    case=False,
                    na=False
                )
            ]

        self.clear_scroll()

        columns = [
            "ID",
            "NAME",
            "SPORTANLAGE",
            "TRAININGSZONEN",
            "AKTIV"
        ]

        self.create_header(columns)

        for _, row in df.iterrows():

            row_data = row.to_dict()

            self.create_row(
                [
                    row.get("place_id", ""),
                    row.get("name", ""),
                    row.get("facility_name", ""),
                    row.get("training_zones", ""),
                    "Ja" if row.get("active") else "Nein"
                ],
                row_data=row_data
            )

        self.set_status(
            f"{len(df)} Plätze gefunden"
        )

    def neuer_platz(self):

        self.edit_place()

    def edit_place(self, daten=None):

        neue_daten = PlaceDialog(
            self,
            title="Platz",
            daten=daten
        ).show()

        if neue_daten is None:
            return

        if daten:
            neue_daten["place_id"] = daten["place_id"]
            neue_daten["active"] = daten.get("active", True)

        self.service.save_place(
            neue_daten
        )

        self.refresh()

        messagebox.showinfo(
            "Gespeichert",
            f"Platz '{neue_daten.get('name', neue_daten.get('NAME', ''))}' wurde gespeichert.",
            parent=self
        )

    def bearbeiten_platz(self):

        selected = self.get_selected_data()

        if selected is None:
            messagebox.showwarning(
                "Kein Platz",
                "Bitte zuerst einen Platz auswählen.",
                parent=self
            )
            return

        self.edit_place(selected) 

    def archivieren_platz(self):

        selected = self.get_selected_data()

        if selected is None:
            messagebox.showwarning(
                "Kein Platz",
                "Bitte zuerst einen Platz auswählen.",
                parent=self
            )
            return

        if not messagebox.askyesno(
            "Archivieren",
            f"Soll der Platz '{selected['name']}' archiviert werden?",
            parent=self
        ):
            return

        self.service.archive_place(
            selected["place_id"]
        )

        self.refresh()

        messagebox.showinfo(
            "Archiviert",
            "Der Platz wurde archiviert.",
            parent=self
        )