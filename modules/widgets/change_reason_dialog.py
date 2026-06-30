import customtkinter as ctk


class ChangeReasonDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        title="Änderung dokumentieren",
        reasons=None
    ):
        super().__init__(parent)

        self.result = None

        if reasons is None:
            reasons = [
                "Tippfehler korrigiert",
                "Daten aktualisiert",
                "Vereinsentscheidung",
                "Saisonwechsel",
                "Sonstiges"
            ]

        self.title(title)
        self.geometry("480x380")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="📝 Änderung dokumentieren",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Grund"
        ).pack(anchor="w", padx=30)

        self.reason = ctk.CTkComboBox(
            self,
            values=reasons,
            width=350
        )
        self.reason.pack(padx=30, pady=(5, 15))
        self.reason.set(reasons[0])

        ctk.CTkLabel(
            self,
            text="Bemerkung"
        ).pack(anchor="w", padx=30)

        self.note = ctk.CTkTextbox(
            self,
            width=350,
            height=100
        )
        self.note.pack(padx=30, pady=(5, 20))

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Abbrechen",
            command=self.cancel
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Speichern",
            command=self.ok
        ).pack(side="left", padx=10)

    def ok(self):

        self.result = {
            "grund": self.reason.get(),
            "bemerkung": self.note.get("1.0", "end").strip()
        }

        self.destroy()

    def cancel(self):

        self.result = None
        self.destroy()