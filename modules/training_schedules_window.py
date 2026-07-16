import customtkinter as ctk
from tkinter import messagebox

from modules.training_schedule_service import TrainingScheduleService
from modules.training_schedule_window import TrainingScheduleWindow
from modules.widgets.list_window_base import ListWindowBase


class TrainingSchedulesWindow(ListWindowBase):

    COLUMNS = [
        "Mannschaft",
        "Saison",
        "Wochentag",
        "Beginn",
        "Ende",
        "Platz",
        "Zone",
        "Trainingsart"
    ]

    def __init__(
        self,
        parent,
        excel_datei
    ):
        self.excel_datei = excel_datei
        self.service = TrainingScheduleService()
        self.all_schedules = []

        super().__init__(
            parent=parent,
            title="Trainingspläne",
            icon="📅",
            search_placeholder="Trainingspläne suchen...",
            search_callback=self.search_schedules
        )

        self.add_toolbar_button(
            "➕ Neu",
            self.open_new_schedule
        )

        self.add_toolbar_button(
            "✏ Bearbeiten",
            self.open_selected_schedule
        )

        self.add_toolbar_button(
            "🗃 Archivieren",
            self.archive_selected_schedule
        )

        self.add_toolbar_button(
            "🔄 Aktualisieren",
            self.refresh
        )

        self.table.double_click_callback = (
            self.open_selected_schedule
        )

        self.load_data()

    def load_data(self):

        try:
            df = self.service.load_schedules_with_names(
                self.excel_datei
            )

        except Exception as error:
            messagebox.showerror(
                "Fehler beim Laden",
                str(error),
                parent=self
            )
            return

        self.all_schedules = []

        if not df.empty:
            self.all_schedules = [
                row.to_dict()
                for _, row in df.iterrows()
            ]

        self.show_schedules(
            self.all_schedules
        )

    def show_schedules(self, schedules):

        self.clear_scroll()
        self.create_header(self.COLUMNS)

        for row in schedules:

            place_name = self.clean_value(
                row.get("PLACE_NAME", "")
            )

            facility_name = self.clean_value(
                row.get("FACILITY_NAME", "")
            )

            if facility_name:
                place_display = (
                    f"{place_name} ({facility_name})"
                )
            else:
                place_display = place_name

            self.create_row(
                [
                    self.clean_value(
                        row.get("TEAM_NAME", "")
                    ),
                    self.clean_value(
                        row.get("SAISON", "")
                    ),
                    self.clean_value(
                        row.get("WOCHENTAG", "")
                    ),
                    self.format_time(
                        row.get("BEGINN", "")
                    ),
                    self.format_time(
                        row.get("ENDE", "")
                    ),
                    place_display,
                    self.clean_value(
                        row.get("ZONE", "")
                    ),
                    self.clean_value(
                        row.get("TRAINING_TYPE", "")
                    )
                ],
                row_data=row
            )

        count = len(schedules)

        if count == 0:
            self.set_status(
                "Keine Trainingspläne vorhanden"
            )
        elif count == 1:
            self.set_status(
                "1 Trainingsplan"
            )
        else:
            self.set_status(
                f"{count} Trainingspläne"
            )

    def search_schedules(self, search_text):

        search_text = str(
            search_text
        ).strip().lower()

        if not search_text:
            self.show_schedules(
                self.all_schedules
            )
            return

        filtered = []

        for row in self.all_schedules:

            searchable_values = [
                row.get("TEAM_NAME", ""),
                row.get("SAISON", ""),
                row.get("WOCHENTAG", ""),
                row.get("BEGINN", ""),
                row.get("ENDE", ""),
                row.get("PLACE_NAME", ""),
                row.get("FACILITY_NAME", ""),
                row.get("ZONE", ""),
                row.get("TRAINING_TYPE", ""),
                row.get("BEMERKUNG", "")
            ]

            searchable_text = " ".join(
                self.clean_value(value)
                for value in searchable_values
            ).lower()

            if search_text in searchable_text:
                filtered.append(row)

        self.show_schedules(filtered)

    def open_new_schedule(self):

        TrainingScheduleWindow(
            self,
            excel_datei=self.excel_datei,
            on_saved=self.load_data
        )

    def open_selected_schedule(
        self,
        schedule_data=None
    ):

        if schedule_data is None:
            schedule_data = (
                self.get_selected_data()
            )

        if not schedule_data:
            messagebox.showwarning(
                "Kein Trainingsplan",
                "Bitte zuerst einen Trainingsplan auswählen.",
                parent=self
            )
            return

        TrainingScheduleWindow(
            self,
            excel_datei=self.excel_datei,
            on_saved=self.load_data,
            schedule_data=schedule_data
        )

    def archive_selected_schedule(self):

        schedule_data = self.get_selected_data()

        if not schedule_data:
            messagebox.showwarning(
                "Kein Trainingsplan",
                "Bitte zuerst einen Trainingsplan auswählen.",
                parent=self
            )
            return

        schedule_id = self.clean_value(
            schedule_data.get(
                "SCHEDULE_ID",
                ""
            )
        )

        team_name = self.clean_value(
            schedule_data.get(
                "TEAM_NAME",
                ""
            )
        )

        weekday = self.clean_value(
            schedule_data.get(
                "WOCHENTAG",
                ""
            )
        )

        if not schedule_id:
            messagebox.showerror(
                "Fehlende ID",
                "Der ausgewählte Trainingsplan besitzt keine SCHEDULE_ID.",
                parent=self
            )
            return

        if not messagebox.askyesno(
            "Trainingsplan archivieren",
            (
                f"Soll der Trainingsplan von "
                f"'{team_name}' am {weekday} "
                f"wirklich archiviert werden?"
            ),
            parent=self
        ):
            return

        try:
            self.service.archive_schedule(
                self.excel_datei,
                schedule_id
            )

        except Exception as error:
            messagebox.showerror(
                "Fehler beim Archivieren",
                str(error),
                parent=self
            )
            return

        self.load_data()

        messagebox.showinfo(
            "Trainingsplan archiviert",
            "Der Trainingsplan wurde archiviert.",
            parent=self
        )

    @staticmethod
    def clean_value(value):

        if value is None:
            return ""

        text = str(value).strip()

        if text.lower() == "nan":
            return ""

        return text

    @classmethod
    def format_time(cls, value):

        text = cls.clean_value(value)

        if not text:
            return ""

        if " " in text:
            text = text.split(" ")[-1]

        if len(text) >= 5:
            return text[:5]

        return text
