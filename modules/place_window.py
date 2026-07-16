import customtkinter as ctk

from modules.widgets.list_window_base import ListWindowBase
from modules.place_service import PlaceService
from modules.place_dialog import PlaceDialog
from tkinter import messagebox



class PlaceWindow(ListWindowBase):

    def __init__(self, parent, excel_datei):

        self.excel_datei = excel_datei

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

        df = self.service.load_places_with_facility_name(
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
            "PLACE_ID",
            "NAME",
            "NAME_FACILITY",
            "TRAININGSZONEN",
            "AKTIV"
        ]

        self.create_header(columns)

        for _, row in df.iterrows():

            row_data = row.to_dict()

            self.create_row(
                [
                    row.get("PLACE_ID", ""),
                    row.get("NAME", ""),
                    row.get("NAME_FACILITY", ""),
                    row.get("TRAININGSZONEN", ""),
                    row.get("AKTIV", "")
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
            self.excel_datei,
            title="Platz",
            daten=daten
        ).show()

        if neue_daten is None:
            return

        if daten:
            neue_daten["PLACE_ID"] = daten["PLACE_ID"]
            neue_daten["AKTIV"] = daten.get("AKTIV", "Ja")

        self.service.save_place(
            self.excel_datei,
            neue_daten
        )

        self.refresh()

        messagebox.showinfo(
            "Gespeichert",
            f"Platz '{neue_daten['NAME']}' wurde gespeichert.",
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
            f"Soll der Platz '{selected['NAME']}' archiviert werden?",
            parent=self
        ):
            return

        self.service.archive_place(
            self.excel_datei,
            selected["PLACE_ID"]
        )

        self.refresh()

        messagebox.showinfo(
            "Archiviert",
            "Der Platz wurde archiviert.",
            parent=self
        )