import customtkinter as ctk


class TrainingPlanWindow(ctk.CTkToplevel):

    def __init__(self, parent, excel_datei):

        super().__init__(parent)

        self.excel_datei = excel_datei

        self.title("Trainingsplan")
        self.geometry("1200x750")
        self.minsize(900, 600)
        self.grab_set()

        self.bind(
            "<Escape>",
            lambda event: self.destroy()
        )

        ctk.CTkLabel(
            self,
            text="⚽ Trainingsplan",
            font=("Segoe UI", 26, "bold")
        ).pack(
            pady=(20, 10)
        )

        ctk.CTkLabel(
            self,
            text="Wochenübersicht der Trainings",
            font=("Segoe UI", 14)
        ).pack(
            pady=(0, 15)
        )

        self.plan_frame = ctk.CTkScrollableFrame(
            self,
            orientation="horizontal"
        )

        self.plan_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # self.create_week_columns()

        self.create_day_grid(
            self.plan_frame
        )

        ctk.CTkButton(
            self,
            text="Schließen",
            command=self.destroy
        ).pack(
            pady=(5, 20)
        )

    def create_week_columns(self):

        weekdays = [
            "Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag"
        ]

        for weekday in weekdays:

            column = ctk.CTkFrame(
                self.plan_frame,
                width=210
            )

            column.pack(
                side="left",
                fill="y",
                padx=5,
                pady=5
            )

            column.pack_propagate(False)

            ctk.CTkLabel(
                column,
                text=weekday,
                font=("Segoe UI", 17, "bold")
            ).pack(
                fill="x",
                padx=10,
                pady=(12, 8)
            )

            placeholder = ctk.CTkFrame(
                column,
                height=90
            )

            placeholder.pack(
                fill="x",
                padx=10,
                pady=10
            )

            placeholder.pack_propagate(False)

            ctk.CTkLabel(
                placeholder,
                text="+ Training hinzufügen",
                font=("Segoe UI", 14, "bold")
            ).pack(
                expand=True
            )

    def create_day_grid(self, parent):

        places = [
            "Hauptplatz",
            "Trainingsplatz",
            "Hinter Tor",
            "Oberer Platz",
            "Funcourt"
        ]

        times = [
            "17:00",
            "17:30",
            "18:00",
            "18:30",
            "19:00",
            "19:30",
            "20:00"
        ]

        grid = ctk.CTkFrame(parent)

        grid.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Kopfzeile
        ctk.CTkLabel(
            grid,
            text="Zeit",
            width=70,
            font=("Segoe UI", 13, "bold")
        ).grid(row=0, column=0, padx=2, pady=2)

        for col, place in enumerate(places, start=1):

            ctk.CTkLabel(
                grid,
                text=place,
                width=120,
                font=("Segoe UI", 13, "bold")
            ).grid(row=0, column=col, padx=2, pady=2)

        for row, time in enumerate(times, start=1):

            ctk.CTkLabel(
                grid,
                text=time,
                width=70
            ).grid(row=row, column=0, padx=2, pady=2)

            for col in range(1, len(places)+1):

                btn = ctk.CTkButton(
                    grid,
                    text="",
                    width=120,
                    height=40
                )

                btn.grid(
                    row=row,
                    column=col,
                    padx=2,
                    pady=2
                )        