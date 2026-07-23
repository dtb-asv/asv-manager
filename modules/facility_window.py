import customtkinter as ctk
import pandas as pd

from modules.widgets.list_window_base import ListWindowBase
from modules.facility_service import FacilityService
from modules.facility_dialog import FacilityDialog
from tkinter import messagebox



class FacilityWindow(ListWindowBase):

    def __init__(self, parent):

        self.service = FacilityService()

        super().__init__(
            parent,
            title="Sportanlagen",
            icon="🏟",
            search_placeholder="Sportanlage suchen...",
            search_callback=self.load_data
        )

        self.add_toolbar_button(
            "➕ Neu",
            self.neue_sportanlage
        )

        self.add_toolbar_button(
            "✏ Bearbeiten",
            self.bearbeiten_sportanlage
        )

        self.add_toolbar_button(
            "📦 Archivieren",
            self.archivieren_sportanlage
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
            "ADRESSE",
            "AKTIV"
        ]

        self.create_header(columns)

        for _, row in df.iterrows():

            row_data = row.to_dict()

            self.create_row(
                [
                    row.get("facility_id", ""),
                    row.get("name", ""),
                    row.get("address", ""),
                    "Ja" if row.get("active") else "Nein"
                ],
                row_data=row_data
            )

        self.set_status(
            f"{len(df)} Sportanlagen gefunden"
        )
    def neue_sportanlage(self):

        self.edit_facility()

    def edit_facility(self, daten=None):

        neue_daten = FacilityDialog(
            self,
            title="Sportanlage",
            daten=daten
        ).show()

        if neue_daten is None:
            return

        if daten:
            neue_daten["facility_id"] = daten["facility_id"]
            neue_daten["active"] = daten.get("active", True)

        self.service.save_facility(
            neue_daten
        )

        self.refresh()

        messagebox.showinfo(
            "Gespeichert",
            f"Sportanlage '{neue_daten['name']}' wurde gespeichert.",
            parent=self
        )

    def bearbeiten_sportanlage(self):

        selected = self.get_selected_data()

        if selected is None:
            messagebox.showwarning(
                "Kein Bereich",
                "Bitte zuerst eine Sportanlage auswählen.",
                parent=self
            )
            return

        self.edit_facility(selected)

    def archivieren_sportanlage(self):

        selected = self.get_selected_data()

        if selected is None:

            messagebox.showwarning(
                "Keine Sportanlage",
                "Bitte zuerst eine Sportanlage auswählen.",
                parent=self
            )
            return

        if not messagebox.askyesno(
            "Archivieren",
            f"Soll die Sportanlage '{selected["name"]}' archiviert werden?",
            parent=self
        ):
            return

        self.service.archive_facility(
            selected["facility_id"]
        )

        self.refresh()

        messagebox.showinfo(
            "Archiviert",
            "Die Sportanlage wurde archiviert.",
            parent=self
        )      