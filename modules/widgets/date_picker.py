import calendar
from datetime import date, datetime

import customtkinter as ctk


class DatePicker(ctk.CTkFrame):
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, parent, width=400, default_date=None, allow_empty=False, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.allow_empty = allow_empty
        self.popup = None

        self.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self, placeholder_text="TT.MM.JJJJ")
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.calendar_button = ctk.CTkButton(
            self,
            text="📅",
            width=44,
            command=self.open_calendar
        )
        self.calendar_button.grid(row=0, column=1)

        self.configure(width=width)

        if default_date is None and not allow_empty:
            default_date = date.today()

        if default_date is not None:
            self.set_date(default_date)

    def get(self):
        return self.entry.get().strip()

    def set(self, value):
        self.set_date(value)

    def clear(self):
        self.entry.delete(0, "end")

    def get_date(self):
        text = self.get()

        if not text:
            if self.allow_empty:
                return None
            raise ValueError("Bitte ein Datum auswählen.")

        try:
            return datetime.strptime(text, self.DATE_FORMAT).date()
        except ValueError as error:
            raise ValueError(
                "Das Datum muss im Format TT.MM.JJJJ eingegeben werden."
            ) from error

    def set_date(self, value):
        if value is None or str(value).strip() == "":
            self.clear()
            return

        parsed_date = self._parse_date(value)
        self.entry.delete(0, "end")
        self.entry.insert(0, parsed_date.strftime(self.DATE_FORMAT))

    def _parse_date(self, value):
        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        text = str(value).strip()
        if not text:
            raise ValueError("Das Datum darf nicht leer sein.")

        for date_format in ("%d.%m.%Y", "%Y-%m-%d", "%d.%m.%y"):
            try:
                return datetime.strptime(text[:10], date_format).date()
            except ValueError:
                continue

        raise ValueError(f"Ungültiges Datum: {text}")

    def open_calendar(self):
        if self.popup is not None and self.popup.winfo_exists():
            self.popup.focus()
            return

        try:
            selected_date = self.get_date()
        except ValueError:
            selected_date = date.today()

        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Datum auswählen")
        self.popup.geometry("340x330")
        self.popup.resizable(False, False)
        self.popup.transient(self.winfo_toplevel())
        self.popup.grab_set()
        self.popup.protocol("WM_DELETE_WINDOW", self._close_popup)

        self.current_year = selected_date.year
        self.current_month = selected_date.month

        self.calendar_frame = ctk.CTkFrame(self.popup)
        self.calendar_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self._draw_calendar()

    def _draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=7, sticky="ew", pady=(5, 15))
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            header,
            text="◀",
            width=40,
            command=self._previous_month
        ).grid(row=0, column=0)

        german_months = [
            "", "Jänner", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
        ]
        month_name = f"{german_months[self.current_month]} {self.current_year}"

        ctk.CTkLabel(
            header,
            text=month_name,
            font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=1, padx=10)

        ctk.CTkButton(
            header,
            text="▶",
            width=40,
            command=self._next_month
        ).grid(row=0, column=2)

        for column, weekday in enumerate(["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]):
            ctk.CTkLabel(
                self.calendar_frame,
                text=weekday,
                font=("Segoe UI", 12, "bold")
            ).grid(row=1, column=column, padx=2, pady=(0, 6))

        month_data = calendar.monthcalendar(self.current_year, self.current_month)

        for row_index, week in enumerate(month_data, start=2):
            for column_index, day_number in enumerate(week):
                if day_number == 0:
                    continue

                ctk.CTkButton(
                    self.calendar_frame,
                    text=str(day_number),
                    width=38,
                    height=32,
                    command=lambda day=day_number: self._select_day(day)
                ).grid(row=row_index, column=column_index, padx=2, pady=2)

        for column in range(7):
            self.calendar_frame.grid_columnconfigure(column, weight=1)

        ctk.CTkButton(
            self.calendar_frame,
            text="Heute",
            command=self._select_today
        ).grid(row=8, column=0, columnspan=7, sticky="ew", padx=4, pady=(12, 4))

    def _previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._draw_calendar()

    def _next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._draw_calendar()

    def _select_day(self, day_number):
        selected_date = date(self.current_year, self.current_month, day_number)
        self.set_date(selected_date)
        self._close_popup()

    def _select_today(self):
        self.set_date(date.today())
        self._close_popup()

    def _close_popup(self):
        if self.popup is not None and self.popup.winfo_exists():
            self.popup.grab_release()
            self.popup.destroy()
        self.popup = None
