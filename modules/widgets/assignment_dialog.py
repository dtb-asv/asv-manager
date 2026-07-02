import customtkinter as ctk


class AssignmentDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        title="Zuordnung"
    ):

        super().__init__(parent)

        self.title(title)
        self.geometry("950x600")

        self.grab_set()

        # ---------- Überschrift ----------

        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)

        # ---------- Hauptbereich ----------

        content = ctk.CTkFrame(self)
        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=0)
        content.grid_columnconfigure(2, weight=1)
        content.grid_rowconfigure(1, weight=1)

        # ---------- Überschriften ----------

        ctk.CTkLabel(
            content,
            text="Verfügbar",
            font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=0, pady=10)

        ctk.CTkLabel(
            content,
            text="Zugeordnet",
            font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=2, pady=10)

        # ---------- Linke Liste ----------

        self.left_list = ctk.CTkTextbox(
            content,
            width=320
        )

        self.left_list.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10
        )

        # ---------- Buttons ----------

        button_frame = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        button_frame.grid(
            row=1,
            column=1,
            padx=10
        )

        ctk.CTkButton(
            button_frame,
            text="▶"
        ).pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="◀"
        ).pack(pady=10)

        # ---------- Rechte Liste ----------

        self.right_list = ctk.CTkTextbox(
            content,
            width=320
        )

        self.right_list.grid(
            row=1,
            column=2,
            sticky="nsew",
            padx=10
        )

        # ---------- Buttons unten ----------

        bottom = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            pady=15
        )

        ctk.CTkButton(
            bottom,
            text="Abbrechen",
            command=self.destroy
        ).pack(
            side="left",
            padx=20
        )

        ctk.CTkButton(
            bottom,
            text="Übernehmen"
        ).pack(
            side="right",
            padx=20
        )