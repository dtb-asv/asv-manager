import customtkinter as ctk

from modules.widgets.list_window_base import ListWindowBase
from modules.facility_service import FacilityService
from modules.facility_dialog import FacilityDialog
from tkinter import messagebox



class FacilityWindow(ListWindowBase):

    def __init__(self, parent, excel_datei):

        self.excel_datei = excel_datei

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

        df = self.service.load_facilities(
            self.excel_datei
        )

        if suchtext:
            df = df[
                df["NAME"].str.contains(
                    suchtext,
                    case=False,
                    na=False
                )
            ]

        self.clear_scroll()

        columns = [
            "FACILITY_ID",
            "NAME",
            "AKTIV"
        ]

        self.create_header(columns)

        for _, row in df.iterrows():

            row_data = row.to_dict()

            self.create_row(
                [
                    row.get("FACILITY_ID", ""),
                    row.get("NAME", ""),
                    row.get("AKTIV", "")
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
            neue_daten["FACILITY_ID"] = daten["FACILITY_ID"]
            neue_daten["AKTIV"] = daten.get("AKTIV", "Ja")

        self.service.save_facility(
            self.excel_datei,
            neue_daten
        )

        self.refresh()

        messagebox.showinfo(
            "Gespeichert",
            f"Sportanlage '{neue_daten['NAME']}' wurde gespeichert.",
            parent=self
        )

    def bearbeiten_sportanlage(self):

        if not hasattr(self, "selected_data") or self.selected_data is None:
            messagebox.showwarning(
                "Kein Bereich",
                "Bitte zuerst eine Sportanlage auswählen.",
                parent=self
            )
            return

        self.edit_facility(self.selected_data)  

    def archivieren_sportanlage(self):

        if not hasattr(self, "selected_data") or self.selected_data is None:

            messagebox.showwarning(
                "Keine Sportanlage",
                "Bitte zuerst eine Sportanlage auswählen.",
                parent=self
            )
            return

        if not messagebox.askyesno(
            "Archivieren",
            f"Soll die Sportanlage '{self.selected_data['NAME']}' archiviert werden?",
            parent=self
        ):
            return

        self.service.archive_facility(
            self.excel_datei,
            self.selected_data["FACILITY_ID"]
        )

        self.refresh()

        messagebox.showinfo(
            "Archiviert",
            "Die Sportanlage wurde archiviert.",
            parent=self
        )      