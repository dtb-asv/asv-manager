import customtkinter as ctk
from tkcalendar import DateEntry


class CalendarEntry(ctk.CTkFrame):

    def __init__(self, parent, label_text="Datum"):
        super().__init__(parent)

        ctk.CTkLabel(
            self,
            text=label_text
        ).pack(anchor="w")

        self.date_entry = DateEntry(
            self,
            date_pattern="dd.mm.yyyy",
            font=("Segoe UI", 12)
        )

        self.date_entry.pack(
            fill="x",
            expand=True,
            pady=(3, 8)
        )

    def get(self):
        return self.date_entry.get()

    def set(self, value):
        if value:
            self.date_entry.set_date(value)