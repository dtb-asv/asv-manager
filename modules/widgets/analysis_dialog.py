import customtkinter as ctk


class AnalysisDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        title,
        analysis
    ):
        super().__init__(parent)

        self.result = False

        self.title(title)
        self.geometry("450x380")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.cancel
        )

        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 20, "bold")
        ).pack(
            pady=(20, 15)
        )

        info = ctk.CTkFrame(self)
        info.pack(
            fill="x",
            padx=20
        )

        self.add_row(
            info,
            0,
            "Erzeugt:",
            analysis.get("generated", 0)
        )

        self.add_row(
            info,
            1,
            "Bereits vorhanden:",
            analysis.get("existing", 0)
        )

        self.add_row(
            info,
            2,
            "Neu:",
            analysis.get("new", 0)
        )

        self.add_row(
            info,
            3,
            "Warnungen:",
            len(
                analysis.get(
                    "warnings",
                    []
                )
            )
        )

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=25
        )

        ctk.CTkButton(
            button_frame,
            text="Abbrechen",
            width=120,
            command=self.cancel
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            button_frame,
            text="Ausführen",
            width=120,
            command=self.ok
        ).pack(
            side="left",
            padx=10
        )

    def add_row(
        self,
        parent,
        row,
        text,
        value
    ):

        ctk.CTkLabel(
            parent,
            text=text,
            anchor="w"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=10,
            pady=8
        )

        ctk.CTkLabel(
            parent,
            text=str(value),
            anchor="e",
            font=("Segoe UI", 13, "bold")
        ).grid(
            row=row,
            column=1,
            sticky="e",
            padx=10,
            pady=8
        )

    def ok(self):
        self.result = True
        self.destroy()

    def cancel(self):
        self.result = False
        self.destroy()

    @staticmethod
    def show(
        parent,
        title,
        analysis
    ):

        dialog = AnalysisDialog(
            parent,
            title,
            analysis
        )

        dialog.wait_window()

        return dialog.result