import customtkinter as ctk


class WarningDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        title,
        warnings
    ):
        super().__init__(parent)

        self.result = False

        self.title(title)
        self.geometry("620x420")
        self.minsize(560, 350)

        self.transient(parent)
        self.grab_set()

        self.bind(
            "<Escape>",
            lambda event: self.cancel()
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.cancel
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # -----------------------------
        # Titel
        # -----------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            header,
            text="⚠ Warnung",
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=title,
            font=("Segoe UI", 14)
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # -----------------------------
        # Warnungen
        # -----------------------------

        frame = ctk.CTkScrollableFrame(
            self
        )

        frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10
        )

        for warning in warnings:

            ctk.CTkLabel(
                frame,
                text="• " + str(warning),
                justify="left",
                anchor="w",
                wraplength=520
            ).pack(
                anchor="w",
                pady=4,
                padx=10
            )

        # -----------------------------
        # Buttons
        # -----------------------------

        footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(10, 20)
        )

        ctk.CTkButton(
            footer,
            text="Abbrechen",
            width=140,
            command=self.cancel
        ).pack(
            side="right",
            padx=(10, 0)
        )

        ctk.CTkButton(
            footer,
            text="Trotzdem speichern",
            width=180,
            command=self.confirm
        ).pack(
            side="right"
        )

    def confirm(self):

        self.result = True
        self.destroy()

    def cancel(self):

        self.result = False
        self.destroy()

    @classmethod
    def show(
        cls,
        parent,
        title,
        warnings
    ):

        dialog = cls(
            parent,
            title,
            warnings
        )

        dialog.wait_window()

        return dialog.result