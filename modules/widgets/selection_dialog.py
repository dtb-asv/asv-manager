import customtkinter as ctk


class SelectionDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        title,
        values
    ):
        super().__init__(parent)

        self.title(title)
        self.geometry("500x600")
        self.grab_set()

        self.result = None
        self.values = values

        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        self.search = ctk.CTkEntry(
            self,
            placeholder_text="Suchen..."
        )

        self.search.pack(
            fill="x",
            padx=20
        )

        self.listbox = ctk.CTkTextbox(
            self,
            height=400
        )

        self.listbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        for value in values:

            self.listbox.insert(
                "end",
                value + "\n"
            )

        ctk.CTkButton(
            self,
            text="Schließen",
            command=self.destroy
        ).pack(
            pady=10
        )