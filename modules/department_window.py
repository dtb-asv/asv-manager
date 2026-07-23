import customtkinter as ctk
import pandas as pd

from modules.widgets.list_window_base import ListWindowBase
from modules.department_service import DepartmentService
from modules.department_dialog import DepartmentDialog
from tkinter import messagebox



class DepartmentWindow(ListWindowBase):

    def __init__(self, parent):

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
            "AKTIV"
        ]

        self.create_header(columns)

        for _, row in df.iterrows():

            row_data = row.to_dict()

            self.create_row(
                [
                    row.get("department_id", ""),
                    row.get("name", ""),
                    "Ja" if row.get("active") else "Nein"
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
            neue_daten["department_id"] = daten["department_id"]
            neue_daten["active"] = daten.get("active", True)

        self.service.save_department(
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
            f"Soll der Bereich '{selected["name"]}' archiviert werden?",
            parent=self
        ):
            return

        self.service.archive_department(
            selected["department_id"]
        )

        self.refresh()

        messagebox.showinfo(
            "Archiviert",
            "Der Bereich wurde archiviert.",
            parent=self
        )      