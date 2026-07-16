import customtkinter as ctk

from modules.widgets.list_window_base import ListWindowBase
from modules.department_service import DepartmentService
from modules.department_dialog import DepartmentDialog
from tkinter import messagebox



class DepartmentWindow(ListWindowBase):

    def __init__(self, parent, excel_datei):

        self.service = DepartmentService()

        super().__init__(
            parent,
            title="Bereiche",
            icon="🏢",
            search_placeholder="Bereich suchen...",
            search_callback=self.load_data
        )

        self.add_toolbar_button(
            "➕ Neu",
            self.neuer_bereich
        )

        self.add_toolbar_button(
            "✏ Bearbeiten",
            self.bearbeiten_bereich
        )

        self.add_toolbar_button(
            "📦 Archivieren",
            self.archivieren_bereich
        )

        self.add_toolbar_button(
            "🔄 Aktualisieren",
            self.refresh
        )

        self.excel_datei = excel_datei

        self.load_data()

    def load_data(self, suchtext=""):

        df = self.service.load_departments(
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
            "DEPARTMENT_ID",
            "NAME",
            "AKTIV"
        ]

        self.create_header(columns)

        for _, row in df.iterrows():

            row_data = row.to_dict()

            self.create_row(
                [
                    row.get("DEPARTMENT_ID", ""),
                    row.get("NAME", ""),
                    row.get("AKTIV", "")
                ],
                row_data=row_data
            )

        self.set_status(
            f"{len(df)} Bereiche gefunden"
        )

    def neuer_bereich(self):

        self.edit_department()

    def edit_department(self, daten=None):

        neue_daten = DepartmentDialog(
            self,
            title="Bereich",
            daten=daten
        ).show()

        if neue_daten is None:
            return

        if daten:
            neue_daten["DEPARTMENT_ID"] = daten["DEPARTMENT_ID"]
            neue_daten["AKTIV"] = daten.get("AKTIV", "Ja")

        self.service.save_department(
            self.excel_datei,
            neue_daten
        )

        self.refresh()

        messagebox.showinfo(
            "Gespeichert",
            f"Bereich '{neue_daten['NAME']}' wurde gespeichert.",
            parent=self
        )

    def bearbeiten_bereich(self):

        selected = self.get_selected_data()

        if selected is None:

            messagebox.showwarning(
                "Kein Bereich",
                "Bitte zuerst einen Bereich auswählen.",
                parent=self
            )
            return

        self.edit_department(selected) 

    def archivieren_bereich(self):

        selected = self.get_selected_data()

        if selected is None:

            messagebox.showwarning(
                "Kein Bereich",
                "Bitte zuerst einen Bereich auswählen.",
                parent=self
            )
            return

        if not messagebox.askyesno(
            "Archivieren",
            f"Soll der Bereich '{selected['NAME']}' archiviert werden?",
            parent=self
        ):
            return

        self.service.archive_department(
            self.excel_datei,
            selected["DEPARTMENT_ID"]
        )

        self.refresh()

        messagebox.showinfo(
            "Archiviert",
            "Der Bereich wurde archiviert.",
            parent=self
        )      